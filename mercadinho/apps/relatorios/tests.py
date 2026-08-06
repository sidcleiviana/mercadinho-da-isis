from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.caixa.models import MovimentacaoFinanceira
from apps.caixa.services import obter_caixa, registrar_movimentacao_financeira
from apps.clientes.models import AtendimentoVirtual, ClienteVirtual
from apps.estoque.services import registrar_entrada_estoque
from apps.produtos.models import Categoria, Produto
from apps.vendas.services import (
    adicionar_produto_por_codigo,
    finalizar_venda,
    iniciar_venda,
)

from .services import (
    relatorio_caixa,
    relatorio_clientes,
    relatorio_estoque,
    relatorio_vendas,
)


class RelatoriosServiceTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Alimentos")
        self.arroz = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789700000001",
            preco_venda=Decimal("10.00"),
            foto="produtos/arroz.jpg",
            categoria=self.categoria,
        )
        self.leite = Produto.objects.create(
            nome="Leite",
            codigo_barras="789700000002",
            preco_venda=Decimal("5.00"),
            foto="produtos/leite.jpg",
            categoria=self.categoria,
        )
        registrar_entrada_estoque(self.arroz, 5, "Entrada inicial")
        registrar_entrada_estoque(self.leite, 1, "Entrada inicial")

    def test_relatorio_vendas_calcula_total_vendido(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.arroz.codigo_barras)
        adicionar_produto_por_codigo(venda, self.leite.codigo_barras)
        finalizar_venda(venda)

        relatorio = relatorio_vendas()

        self.assertEqual(relatorio["total_vendas"], 1)
        self.assertEqual(relatorio["valor_total"], Decimal("15.00"))
        self.assertEqual(
            list(relatorio["produtos_mais_vendidos"])[0]["produto__nome"],
            "Arroz",
        )

    def test_relatorio_caixa_exibe_saldo_entradas_e_saidas(self):
        registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.ENTRADA,
            Decimal("20.00"),
            "Entrada manual",
        )
        registrar_movimentacao_financeira(
            MovimentacaoFinanceira.Tipo.SAIDA,
            Decimal("5.00"),
            "Saida manual",
        )

        relatorio = relatorio_caixa()

        self.assertEqual(relatorio["saldo_atual"], Decimal("15.00"))
        self.assertEqual(relatorio["total_entradas"], Decimal("20.00"))
        self.assertEqual(relatorio["total_saidas"], Decimal("5.00"))
        self.assertEqual(obter_caixa().saldo_atual, Decimal("15.00"))

    def test_relatorio_estoque_identifica_estoque_baixo_e_saida(self):
        venda = iniciar_venda()
        adicionar_produto_por_codigo(venda, self.arroz.codigo_barras)
        finalizar_venda(venda)

        relatorio = relatorio_estoque()

        self.assertEqual(relatorio["quantidade_total_estoque"], 5)
        self.assertIn(self.leite.estoque, list(relatorio["produtos_estoque_baixo"]))
        self.assertEqual(
            list(relatorio["produtos_maior_saida"])[0]["produto__nome"],
            "Arroz",
        )

    def test_relatorio_clientes_calcula_atendidos_desistentes_e_tempo_medio(self):
        agora = timezone.now()
        ana = ClienteVirtual.objects.create(nome="Ana")
        joao = ClienteVirtual.objects.create(nome="Joao")
        AtendimentoVirtual.objects.create(
            cliente_virtual=ana,
            horario_programado=agora - timedelta(minutes=20),
            horario_inicio=agora - timedelta(minutes=10),
            horario_finalizacao=agora,
            status=AtendimentoVirtual.Status.FINALIZADO,
            valor_total=Decimal("10.00"),
        )
        AtendimentoVirtual.objects.create(
            cliente_virtual=joao,
            horario_programado=agora - timedelta(minutes=15),
            horario_finalizacao=agora,
            status=AtendimentoVirtual.Status.DESISTIU,
            valor_total=Decimal("0.00"),
        )

        relatorio = relatorio_clientes()

        self.assertEqual(relatorio["clientes_atendidos"], 1)
        self.assertEqual(relatorio["clientes_desistentes"], 1)
        self.assertIsNotNone(relatorio["tempo_medio_atendimento"])


class RelatoriosViewsTest(TestCase):
    def test_paginas_de_relatorios_renderizam(self):
        urls = [
            reverse("relatorios:resumo"),
            reverse("relatorios:vendas"),
            reverse("relatorios:caixa"),
            reverse("relatorios:estoque"),
            reverse("relatorios:clientes"),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
