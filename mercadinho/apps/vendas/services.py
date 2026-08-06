from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.caixa.models import MovimentacaoFinanceira
from apps.caixa.services import registrar_movimentacao_financeira
from apps.estoque.models import Estoque, MovimentacaoEstoque
from apps.estoque.services import garantir_estoque_para_produto
from apps.produtos.models import Produto

from .models import ItemVenda, Venda


def gerar_numero_venda():
    return timezone.now().strftime("%Y%m%d%H%M%S%f")


def iniciar_venda(tipo_cliente=Venda.TipoCliente.REAL):
    return Venda.objects.create(
        numero_venda=gerar_numero_venda(),
        data=timezone.now(),
        tipo_cliente=tipo_cliente,
        valor_total=Decimal("0.00"),
        status=Venda.Status.EM_ANDAMENTO,
    )


def obter_venda_em_andamento(venda_id):
    return Venda.objects.prefetch_related("itens__produto").get(
        pk=venda_id,
        status=Venda.Status.EM_ANDAMENTO,
    )


def recalcular_total_venda(venda):
    total = sum((item.valor_total for item in venda.itens.all()), Decimal("0.00"))
    venda.valor_total = total
    venda.save(update_fields=["valor_total", "atualizado_em"])
    return total


def adicionar_produto_por_codigo(venda, codigo_barras):
    codigo = codigo_barras.strip()
    if not codigo:
        raise ValidationError("Informe um codigo de barras.")

    try:
        produto = Produto.objects.select_related("categoria").get(codigo_barras=codigo)
    except Produto.DoesNotExist as exc:
        raise ValidationError("Produto nao encontrado.") from exc

    if not produto.ativo:
        raise ValidationError("Produto inativo nao pode ser vendido.")

    estoque = garantir_estoque_para_produto(produto)
    quantidade_no_carrinho = (
        venda.itens.filter(produto=produto).values_list("quantidade", flat=True).first()
        or 0
    )
    if estoque.quantidade_atual <= quantidade_no_carrinho:
        raise ValidationError("Produto indisponivel em estoque.")

    item, criado = ItemVenda.objects.get_or_create(
        venda=venda,
        produto=produto,
        defaults={
            "quantidade": 1,
            "valor_unitario": produto.preco_venda,
            "valor_total": produto.preco_venda,
        },
    )
    if not criado:
        item.quantidade += 1
        item.valor_total = item.valor_unitario * item.quantidade
        item.save(update_fields=["quantidade", "valor_total", "atualizado_em"])

    venda.refresh_from_db()
    recalcular_total_venda(venda)
    return item


def cancelar_venda(venda):
    if venda.status != Venda.Status.EM_ANDAMENTO:
        raise ValidationError("Apenas vendas em andamento podem ser canceladas.")

    with transaction.atomic():
        venda.status = Venda.Status.CANCELADA
        venda.save(update_fields=["status", "atualizado_em"])
    return venda


def finalizar_venda(venda):
    if venda.status != Venda.Status.EM_ANDAMENTO:
        raise ValidationError("Apenas vendas em andamento podem ser finalizadas.")

    itens = list(venda.itens.select_related("produto"))
    if not itens:
        raise ValidationError("A venda precisa ter pelo menos um item.")

    with transaction.atomic():
        venda = Venda.objects.select_for_update().get(pk=venda.pk)
        itens = list(venda.itens.select_related("produto"))
        total = sum((item.valor_total for item in itens), Decimal("0.00"))

        for item in itens:
            estoque = Estoque.objects.select_for_update().get(produto=item.produto)
            if estoque.quantidade_atual < item.quantidade:
                raise ValidationError(
                    f"Estoque insuficiente para {item.produto.nome}."
                )

        for item in itens:
            Estoque.objects.filter(produto=item.produto).update(
                quantidade_atual=F("quantidade_atual") - item.quantidade
            )
            MovimentacaoEstoque.objects.create(
                produto=item.produto,
                tipo=MovimentacaoEstoque.Tipo.VENDA,
                quantidade=item.quantidade,
                data=timezone.now(),
                observacao=f"Venda {venda.numero_venda}",
            )

        venda.valor_total = total
        venda.status = Venda.Status.CONCLUIDA
        venda.save(update_fields=["valor_total", "status", "atualizado_em"])

        registrar_movimentacao_financeira(
            tipo=MovimentacaoFinanceira.Tipo.ENTRADA,
            valor=total,
            descricao=f"Venda {venda.numero_venda}",
            venda=venda,
        )

    venda.refresh_from_db()
    return venda
