from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.caixa.models import MovimentacaoFinanceira
from apps.caixa.services import obter_caixa
from apps.estoque.models import MovimentacaoEstoque
from apps.estoque.services import registrar_entrada_estoque
from apps.produtos.models import Categoria, Produto

from .models import ItemVenda, Venda
from .services import (
    adicionar_produto_por_codigo,
    cancelar_venda,
    finalizar_venda,
    iniciar_venda,
)


class VendaModelTest(TestCase):
    def test_venda_armazena_item_com_valor_unitario_historico(self):
        categoria = Categoria.objects.create(nome="Alimentos")
        produto = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789300000001",
            preco_venda=Decimal("29.90"),
            foto="produtos/arroz.jpg",
            categoria=categoria,
        )
        venda = Venda.objects.create(
            numero_venda="000001",
            data=timezone.now(),
            tipo_cliente=Venda.TipoCliente.REAL,
            valor_total=Decimal("59.80"),
            status=Venda.Status.CONCLUIDA,
        )
        item = ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=2,
            valor_unitario=Decimal("29.90"),
            valor_total=Decimal("59.80"),
        )

        self.assertEqual(item.venda, venda)
        self.assertEqual(item.produto, produto)
        self.assertEqual(item.valor_unitario, Decimal("29.90"))


class VendaServiceTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Alimentos")
        self.arroz = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789100000100",
            preco_venda=Decimal("29.90"),
            foto="produtos/arroz.jpg",
            categoria=self.categoria,
        )
        self.leite = Produto.objects.create(
            nome="Leite",
            codigo_barras="789200000100",
            preco_venda=Decimal("5.50"),
            foto="produtos/leite.jpg",
            categoria=self.categoria,
        )
        registrar_entrada_estoque(self.arroz, 3, "Entrada inicial")
        registrar_entrada_estoque(self.leite, 2, "Entrada inicial")

    def test_criar_venda_em_andamento(self):
        venda = iniciar_venda()

        self.assertEqual(venda.status, Venda.Status.EM_ANDAMENTO)
        self.assertEqual(venda.tipo_cliente, Venda.TipoCliente.REAL)
        self.assertEqual(venda.valor_total, Decimal("0.00"))

    def test_adicionar_produto_por_codigo_e_calcular_total(self):
        venda = iniciar_venda()

        adicionar_produto_por_codigo(venda, self.arroz.codigo_barras)
        adicionar_produto_por_codigo(venda, self.arroz.codigo_barras)
        venda.refresh_from_db()
        item = venda.itens.get(produto=self.arroz)

        self.assertEqual(item.quantidade, 2)
        self.assertEqual(item.valor_unitario, Decimal("29.90"))
        self.assertEqual(item.valor_total, Decimal("59.80"))
        self.assertEqual(venda.valor_total, Decimal("59.80"))

    def test_produto_inexistente_nao_adiciona_item(self):
        venda = iniciar_venda()

        with self.assertRaises(ValidationError):
            adicionar_produto_por_codigo(venda, "codigo-inexistente")

        self.assertEqual(venda.itens.count(), 0)

    def test_nao_permite_adicionar_acima_do_estoque(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.leite.codigo_barras)
        adicionar_produto_por_codigo(venda, self.leite.codigo_barras)

        with self.assertRaises(ValidationError):
            adicionar_produto_por_codigo(venda, self.leite.codigo_barras)

        self.assertEqual(venda.itens.get(produto=self.leite).quantidade, 2)

    def test_finalizar_venda_atualiza_estoque_caixa_e_historico(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.arroz.codigo_barras)
        adicionar_produto_por_codigo(venda, self.leite.codigo_barras)

        finalizar_venda(venda)
        venda.refresh_from_db()
        self.arroz.estoque.refresh_from_db()
        self.leite.estoque.refresh_from_db()

        self.assertEqual(venda.status, Venda.Status.CONCLUIDA)
        self.assertEqual(venda.valor_total, Decimal("35.40"))
        self.assertEqual(self.arroz.estoque.quantidade_atual, 2)
        self.assertEqual(self.leite.estoque.quantidade_atual, 1)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("35.40"))
        self.assertEqual(
            MovimentacaoEstoque.objects.filter(
                tipo=MovimentacaoEstoque.Tipo.VENDA
            ).count(),
            2,
        )
        self.assertTrue(
            MovimentacaoFinanceira.objects.filter(venda=venda, valor=Decimal("35.40")).exists()
        )

    def test_cancelamento_nao_movimenta_estoque_nem_caixa(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.arroz.codigo_barras)

        cancelar_venda(venda)
        venda.refresh_from_db()
        self.arroz.estoque.refresh_from_db()

        self.assertEqual(venda.status, Venda.Status.CANCELADA)
        self.assertEqual(self.arroz.estoque.quantidade_atual, 3)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("0.00"))
        self.assertEqual(
            MovimentacaoEstoque.objects.filter(
                tipo=MovimentacaoEstoque.Tipo.VENDA
            ).count(),
            0,
        )
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 0)

    def test_finalizacao_com_estoque_insuficiente_reverte_operacao(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.arroz.codigo_barras)
        self.arroz.estoque.quantidade_atual = 0
        self.arroz.estoque.save(update_fields=["quantidade_atual", "atualizado_em"])

        with self.assertRaises(ValidationError):
            finalizar_venda(venda)

        venda.refresh_from_db()
        self.arroz.estoque.refresh_from_db()
        self.assertEqual(venda.status, Venda.Status.EM_ANDAMENTO)
        self.assertEqual(self.arroz.estoque.quantidade_atual, 0)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("0.00"))
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 0)
        self.assertEqual(
            MovimentacaoEstoque.objects.filter(
                tipo=MovimentacaoEstoque.Tipo.VENDA
            ).count(),
            0,
        )


class VendaViewsTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Alimentos")
        self.produto = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789100000200",
            preco_venda=Decimal("29.90"),
            foto="produtos/arroz.jpg",
            categoria=self.categoria,
        )
        registrar_entrada_estoque(self.produto, 2, "Entrada inicial")

    def test_nova_venda_redireciona_para_atendimento(self):
        response = self.client.get(reverse("vendas:nova"))

        venda = Venda.objects.get()
        self.assertRedirects(response, reverse("vendas:atendimento", args=[venda.pk]))
        self.assertEqual(venda.status, Venda.Status.EM_ANDAMENTO)

    def test_adicionar_item_via_codigo_de_barras_na_view(self):
        venda = iniciar_venda()

        response = self.client.post(
            reverse("vendas:adicionar_item", args=[venda.pk]),
            {"codigo_barras": self.produto.codigo_barras},
        )

        self.assertRedirects(response, reverse("vendas:atendimento", args=[venda.pk]))
        venda.refresh_from_db()
        self.assertEqual(venda.itens.get().produto, self.produto)
        self.assertEqual(venda.valor_total, Decimal("29.90"))

    def test_finalizar_venda_pela_view(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.produto.codigo_barras)

        response = self.client.post(reverse("vendas:finalizar", args=[venda.pk]))

        self.assertRedirects(response, reverse("vendas:lista"))
        venda.refresh_from_db()
        self.produto.estoque.refresh_from_db()
        self.assertEqual(venda.status, Venda.Status.CONCLUIDA)
        self.assertEqual(self.produto.estoque.quantidade_atual, 1)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("29.90"))

    def test_cancelar_venda_pela_view_sem_impacto(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.produto.codigo_barras)

        response = self.client.post(reverse("vendas:cancelar", args=[venda.pk]))

        self.assertRedirects(response, reverse("vendas:lista"))
        venda.refresh_from_db()
        self.produto.estoque.refresh_from_db()
        self.assertEqual(venda.status, Venda.Status.CANCELADA)
        self.assertEqual(self.produto.estoque.quantidade_atual, 2)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("0.00"))
