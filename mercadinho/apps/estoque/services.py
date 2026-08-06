from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.produtos.models import Produto

from .models import Estoque, MovimentacaoEstoque


def garantir_estoque_para_produto(produto):
    estoque, _ = Estoque.objects.get_or_create(
        produto=produto,
        defaults={"quantidade_atual": 0},
    )
    return estoque


def garantir_estoques_iniciais():
    produtos_sem_estoque = Produto.objects.filter(estoque__isnull=True)
    for produto in produtos_sem_estoque:
        garantir_estoque_para_produto(produto)


def registrar_entrada_estoque(produto, quantidade, observacao=""):
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    with transaction.atomic():
        estoque = garantir_estoque_para_produto(produto)
        estoque = Estoque.objects.select_for_update().get(pk=estoque.pk)
        movimentacao = MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo=MovimentacaoEstoque.Tipo.ENTRADA,
            quantidade=quantidade,
            data=timezone.now(),
            observacao=observacao,
        )
        Estoque.objects.filter(pk=estoque.pk).update(
            quantidade_atual=F("quantidade_atual") + quantidade
        )
        estoque.refresh_from_db()

    return estoque, movimentacao
