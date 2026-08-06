from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.caixa.models import MovimentacaoFinanceira
from apps.caixa.services import registrar_movimentacao_financeira
from apps.estoque.services import registrar_entrada_estoque
from apps.produtos.models import Categoria, Produto
from apps.vendas.services import adicionar_produto_por_codigo, finalizar_venda, iniciar_venda

from .models import Expediente
from .services import obter_expediente


class DashboardTest(TestCase):
    def test_dashboard_loads(self):
        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mercadinho da Ísis")
        self.assertContains(response, "Expediente")

    def test_abrir_e_fechar_expediente(self):
        abrir_response = self.client.post(reverse("core:abrir_expediente"))
        expediente = obter_expediente()

        self.assertRedirects(abrir_response, reverse("core:dashboard"))
        self.assertEqual(expediente.status, Expediente.Status.ABERTO)
        self.assertIsNotNone(expediente.aberto_em)

        fechar_response = self.client.post(reverse("core:fechar_expediente"))
        expediente.refresh_from_db()

        self.assertRedirects(fechar_response, reverse("core:dashboard"))
        self.assertEqual(expediente.status, Expediente.Status.FECHADO)
        self.assertIsNotNone(expediente.fechado_em)

    def test_dashboard_exibe_indicadores_reais(self):
        categoria = Categoria.objects.create(nome="Alimentos")
        produto = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789100000777",
            preco_venda=Decimal("29.90"),
            foto="produtos/arroz.jpg",
            categoria=categoria,
        )
        registrar_entrada_estoque(produto, 3, "Entrada inicial")
        registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.ENTRADA,
            Decimal("10.00"),
            "Ajuste manual",
        )

        response = self.client.get(reverse("core:dashboard"))

        self.assertContains(response, "Produtos ativos")
        self.assertContains(response, "Produtos em estoque")
        self.assertContains(response, "3")
        self.assertContains(response, "10,00")

    def test_dashboard_exibe_ultima_venda(self):
        categoria = Categoria.objects.create(nome="Bebidas")
        produto = Produto.objects.create(
            nome="Leite",
            codigo_barras="789200000777",
            preco_venda=Decimal("5.50"),
            foto="produtos/leite.jpg",
            categoria=categoria,
        )
        registrar_entrada_estoque(produto, 1, "Entrada inicial")
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, produto.codigo_barras)
        finalizar_venda(venda)

        response = self.client.get(reverse("core:dashboard"))

        self.assertContains(response, "Ultima venda")
        self.assertContains(response, venda.numero_venda)
