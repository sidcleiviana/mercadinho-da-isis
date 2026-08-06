from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .forms import ProdutoForm
from .models import Categoria, Produto


def imagem_teste(nome="produto.png"):
    arquivo = BytesIO()
    imagem = Image.new("RGB", (1, 1), color="white")
    imagem.save(arquivo, format="PNG")
    arquivo.seek(0)
    return SimpleUploadedFile(
        nome,
        arquivo.getvalue(),
        content_type="image/png",
    )


class ProdutoModelTest(TestCase):
    def test_codigo_barras_deve_ser_unico(self):
        categoria = Categoria.objects.create(nome="Alimentos")
        Produto.objects.create(
            nome="Arroz",
            codigo_barras="789100000001",
            preco_venda=Decimal("29.90"),
            foto="produtos/arroz.jpg",
            categoria=categoria,
        )

        with self.assertRaises(IntegrityError):
            Produto.objects.create(
                nome="Arroz Integral",
                codigo_barras="789100000001",
                preco_venda=Decimal("31.90"),
                foto="produtos/arroz-integral.jpg",
                categoria=categoria,
            )


class ProdutoFormTest(TestCase):
    def test_preco_deve_ser_positivo(self):
        categoria = Categoria.objects.create(nome="Alimentos")
        form = ProdutoForm(
            data={
                "nome": "Arroz",
                "categoria": categoria.pk,
                "codigo_barras": "789100000002",
                "preco_venda": "0.00",
                "ativo": "on",
            },
            files={"foto": imagem_teste()},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("preco_venda", form.errors)

    def test_foto_e_obrigatoria_no_cadastro(self):
        categoria = Categoria.objects.create(nome="Alimentos")
        form = ProdutoForm(
            data={
                "nome": "Arroz",
                "categoria": categoria.pk,
                "codigo_barras": "789100000003",
                "preco_venda": "29.90",
                "ativo": "on",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("foto", form.errors)


class ProdutoAdminTest(TestCase):
    def test_produto_e_categoria_estao_registrados_no_admin(self):
        self.assertIn(Produto, admin.site._registry)
        self.assertIn(Categoria, admin.site._registry)


class ProdutoViewsTest(TestCase):
    def setUp(self):
        self.media_dir = TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media_dir.name)
        self.override.enable()
        self.categoria = Categoria.objects.create(nome="Alimentos")

    def tearDown(self):
        self.override.disable()
        self.media_dir.cleanup()

    def criar_produto(self, nome="Arroz", codigo="789100000004"):
        return Produto.objects.create(
            nome=nome,
            codigo_barras=codigo,
            preco_venda=Decimal("29.90"),
            foto="produtos/arroz.png",
            categoria=self.categoria,
        )

    def test_lista_produtos_carrega(self):
        self.criar_produto()

        response = self.client.get(reverse("produtos:lista"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Arroz")

    def test_busca_por_nome_e_codigo_de_barras(self):
        self.criar_produto(nome="Arroz", codigo="789100000005")
        self.criar_produto(nome="Leite", codigo="789200000005")

        response_nome = self.client.get(reverse("produtos:lista"), {"q": "Arroz"})
        response_codigo = self.client.get(reverse("produtos:lista"), {"q": "789200"})

        self.assertContains(response_nome, "Arroz")
        self.assertNotContains(response_nome, "Leite")
        self.assertContains(response_codigo, "Leite")
        self.assertNotContains(response_codigo, "Arroz")

    def test_criacao_de_produto_com_upload_de_imagem(self):
        response = self.client.post(
            reverse("produtos:criar"),
            {
                "nome": "Feijao",
                "categoria": self.categoria.pk,
                "codigo_barras": "789300000001",
                "preco_venda": "12.50",
                "ativo": "on",
                "foto": imagem_teste("feijao.png"),
            },
        )

        self.assertRedirects(response, reverse("produtos:lista"))
        produto = Produto.objects.get(codigo_barras="789300000001")
        self.assertEqual(produto.nome, "Feijao")
        self.assertTrue(produto.foto.name.startswith("produtos/"))

    def test_edicao_de_produto_mantem_foto_existente(self):
        produto = self.criar_produto()

        response = self.client.post(
            reverse("produtos:editar", args=[produto.pk]),
            {
                "nome": "Arroz Integral",
                "categoria": self.categoria.pk,
                "codigo_barras": produto.codigo_barras,
                "preco_venda": "31.90",
                "ativo": "on",
            },
        )

        self.assertRedirects(response, reverse("produtos:lista"))
        produto.refresh_from_db()
        self.assertEqual(produto.nome, "Arroz Integral")
        self.assertEqual(produto.preco_venda, Decimal("31.90"))
        self.assertEqual(produto.foto.name, "produtos/arroz.png")

    def test_visualizacao_de_produto_exibe_detalhes(self):
        produto = self.criar_produto()

        response = self.client.get(reverse("produtos:detalhe", args=[produto.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, produto.nome)
        self.assertContains(response, produto.codigo_barras)
