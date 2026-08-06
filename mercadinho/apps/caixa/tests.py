from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.vendas.models import Venda

from .forms import MovimentacaoFinanceiraForm
from .models import Caixa, MovimentacaoFinanceira
from .services import calcular_saldo, obter_caixa, registrar_movimentacao_financeira


class CaixaModelTest(TestCase):
    def test_deve_existir_apenas_um_caixa(self):
        Caixa.objects.create(saldo_atual=Decimal("0.00"))

        with self.assertRaises(IntegrityError):
            Caixa.objects.create(saldo_atual=Decimal("10.00"))

    def test_saldo_nao_pode_ser_editado_diretamente(self):
        caixa = obter_caixa()
        caixa.saldo_atual = Decimal("100.00")

        with self.assertRaises(ValidationError):
            caixa.save()

    def test_movimentacao_financeira_tem_referencia_opcional_para_venda(self):
        venda = Venda.objects.create(
            numero_venda="000002",
            data=timezone.now(),
            tipo_cliente=Venda.TipoCliente.REAL,
            valor_total=Decimal("15.00"),
            status=Venda.Status.CONCLUIDA,
        )
        movimentacao = MovimentacaoFinanceira.objects.create(
            tipo=MovimentacaoFinanceira.Tipo.ENTRADA,
            valor=Decimal("15.00"),
            descricao="Venda registrada",
            data=timezone.now(),
            venda=venda,
        )

        self.assertEqual(movimentacao.tipo, MovimentacaoFinanceira.Tipo.ENTRADA)
        self.assertEqual(movimentacao.valor, Decimal("15.00"))
        self.assertEqual(movimentacao.venda, venda)


class MovimentacaoFinanceiraFormTest(TestCase):
    def test_valor_deve_ser_positivo(self):
        form = MovimentacaoFinanceiraForm(
            data={"valor": "0.00", "descricao": "Ajuste manual"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("valor", form.errors)

    def test_descricao_e_obrigatoria(self):
        form = MovimentacaoFinanceiraForm(data={"valor": "10.00", "descricao": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)


class CaixaServiceTest(TestCase):
    def test_registrar_entrada_manual_atualiza_saldo_e_historico(self):
        caixa, movimentacao = registrar_movimentacao_financeira(
            tipo=MovimentacaoFinanceira.Tipo.ENTRADA,
            valor=Decimal("50.00"),
            descricao="Ajuste manual",
        )

        self.assertEqual(caixa.saldo_atual, Decimal("50.00"))
        self.assertEqual(movimentacao.tipo, MovimentacaoFinanceira.Tipo.ENTRADA)
        self.assertEqual(calcular_saldo(), Decimal("50.00"))

    def test_registrar_saida_manual_atualiza_saldo_e_historico(self):
        registrar_movimentacao_financeira(
            tipo=MovimentacaoFinanceira.Tipo.ENTRADA,
            valor=Decimal("80.00"),
            descricao="Ajuste manual",
        )
        caixa, movimentacao = registrar_movimentacao_financeira(
            tipo=MovimentacaoFinanceira.Tipo.SAIDA,
            valor=Decimal("30.00"),
            descricao="Reposicao de estoque",
        )

        self.assertEqual(caixa.saldo_atual, Decimal("50.00"))
        self.assertEqual(movimentacao.tipo, MovimentacaoFinanceira.Tipo.SAIDA)
        self.assertEqual(calcular_saldo(), Decimal("50.00"))

    def test_saida_maior_que_saldo_e_bloqueada(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao_financeira(
                tipo=MovimentacaoFinanceira.Tipo.SAIDA,
                valor=Decimal("10.00"),
                descricao="Despesa",
            )

        self.assertEqual(MovimentacaoFinanceira.objects.count(), 0)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("0.00"))

    def test_consistencia_apos_multiplas_operacoes(self):
        registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.ENTRADA,
            Decimal("100.00"),
            "Entrada inicial",
        )
        registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.SAIDA,
            Decimal("25.50"),
            "Despesa administrativa",
        )
        caixa, _ = registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.ENTRADA,
            Decimal("10.25"),
            "Ajuste manual",
        )

        self.assertEqual(caixa.saldo_atual, Decimal("84.75"))
        self.assertEqual(calcular_saldo(), Decimal("84.75"))
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 3)


class CaixaViewsTest(TestCase):
    def test_dashboard_exibe_saldo_e_historico(self):
        registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.ENTRADA,
            Decimal("20.00"),
            "Entrada manual",
        )

        response = self.client.get(reverse("caixa:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Saldo Atual")
        self.assertContains(response, "Entrada manual")
        self.assertContains(response, "20,00")

    def test_view_registra_entrada(self):
        response = self.client.post(
            reverse("caixa:entrada"),
            {"valor": "35.00", "descricao": "Entrada manual"},
        )

        self.assertRedirects(response, reverse("caixa:dashboard"))
        self.assertEqual(obter_caixa().saldo_atual, Decimal("35.00"))

    def test_view_registra_saida(self):
        registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.ENTRADA,
            Decimal("40.00"),
            "Entrada manual",
        )

        response = self.client.post(
            reverse("caixa:saida"),
            {"valor": "15.00", "descricao": "Reposicao de estoque"},
        )

        self.assertRedirects(response, reverse("caixa:dashboard"))
        self.assertEqual(obter_caixa().saldo_atual, Decimal("25.00"))
