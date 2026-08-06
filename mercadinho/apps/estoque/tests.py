from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from apps.produtos.models import Categoria, Produto

from .forms import EntradaEstoqueForm
from .models import Estoque, MovimentacaoEstoque
from .services import registrar_entrada_estoque


class EstoqueModelTest(TestCase):
    def criar_produto(self, nome="Leite", codigo="789200000001"):
        categoria = Categoria.objects.create(nome="Bebidas")
        return Produto.objects.create(
            nome=nome,
            codigo_barras=codigo,
            preco_venda=Decimal("5.50"),
            foto="produtos/leite.jpg",
            categoria=categoria,
        )

    def test_produto_recebe_estoque_inicial_zero(self):
        produto = self.criar_produto()

        self.assertEqual(produto.estoque.quantidade_atual, 0)

    def test_produto_deve_possuir_apenas_um_estoque(self):
        produto = self.criar_produto()

        with self.assertRaises(IntegrityError):
            Estoque.objects.create(produto=produto, quantidade_atual=5)

    def test_entrada_de_estoque_atualiza_quantidade_e_movimentacao(self):
        produto = self.criar_produto()

        estoque, movimentacao = registrar_entrada_estoque(
            produto=produto,
            quantidade=8,
            observacao="Reposicao manual",
        )

        self.assertEqual(estoque.quantidade_atual, 8)
        self.assertEqual(movimentacao.produto, produto)
        self.assertEqual(movimentacao.tipo, MovimentacaoEstoque.Tipo.ENTRADA)
        self.assertEqual(movimentacao.quantidade, 8)
        self.assertEqual(movimentacao.observacao, "Reposicao manual")

    def test_quantidade_invalida_nao_altera_estoque_nem_cria_movimentacao(self):
        produto = self.criar_produto()

        with self.assertRaises(ValueError):
            registrar_entrada_estoque(produto=produto, quantidade=0)

        produto.estoque.refresh_from_db()
        self.assertEqual(produto.estoque.quantidade_atual, 0)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 0)


class EntradaEstoqueFormTest(TestCase):
    def test_quantidade_deve_ser_inteiro_positivo(self):
        form = EntradaEstoqueForm(data={"quantidade": "0", "observacao": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("quantidade", form.errors)


class EstoqueViewsTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Alimentos")
        self.arroz = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789100000010",
            preco_venda=Decimal("29.90"),
            foto="produtos/arroz.jpg",
            categoria=self.categoria,
        )
        self.leite = Produto.objects.create(
            nome="Leite",
            codigo_barras="789200000010",
            preco_venda=Decimal("5.50"),
            foto="produtos/leite.jpg",
            categoria=self.categoria,
        )

    def test_lista_estoque_exibe_produtos_e_quantidades(self):
        response = self.client.get(reverse("estoque:lista"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Arroz")
        self.assertContains(response, "Leite")
        self.assertContains(response, "Quantidade")

    def test_busca_estoque_por_nome_e_codigo(self):
        response_nome = self.client.get(reverse("estoque:lista"), {"q": "Arroz"})
        response_codigo = self.client.get(reverse("estoque:lista"), {"q": "789200"})

        self.assertContains(response_nome, "Arroz")
        self.assertNotContains(response_nome, "Leite")
        self.assertContains(response_codigo, "Leite")
        self.assertNotContains(response_codigo, "Arroz")

    def test_entrada_de_estoque_pela_view(self):
        response = self.client.post(
            reverse("estoque:entrada", args=[self.arroz.pk]),
            {"quantidade": "4", "observacao": "Entrada manual"},
        )

        self.assertRedirects(response, reverse("estoque:lista"))
        self.arroz.estoque.refresh_from_db()
        self.assertEqual(self.arroz.estoque.quantidade_atual, 4)
        self.assertTrue(
            MovimentacaoEstoque.objects.filter(
                produto=self.arroz,
                tipo=MovimentacaoEstoque.Tipo.ENTRADA,
                quantidade=4,
            ).exists()
        )

    def test_historico_exibe_movimentacao(self):
        registrar_entrada_estoque(self.arroz, 3, "Entrada inicial")

        response = self.client.get(reverse("estoque:historico"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Arroz")
        self.assertContains(response, "Entrada inicial")
