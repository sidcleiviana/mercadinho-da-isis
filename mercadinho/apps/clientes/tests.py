from decimal import Decimal
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.caixa.services import obter_caixa
from apps.core.services import abrir_expediente, fechar_expediente
from apps.estoque.services import registrar_entrada_estoque
from apps.produtos.models import Categoria, Produto
from apps.vendas.models import Venda
from apps.vendas.services import adicionar_produto_por_codigo, finalizar_venda

from .models import (
    AtendimentoVirtual,
    ClienteVirtual,
    EventoCliente,
    InteracaoConversa,
    PedidoVirtual,
)
from .services import (
    atendimento_em_andamento,
    cancelar_atendimento,
    clientes_restantes_hoje,
    contexto_conversa,
    fila_ativa,
    finalizar_atendimento_por_venda,
    gerar_atendimentos_do_dia,
    garantir_clientes_iniciais,
    iniciar_atendimento,
    processar_desistencias,
    processar_fluxo_clientes,
    responder_conversa,
)


class AtendimentoVirtualModelTest(TestCase):
    def test_atendimento_virtual_relaciona_cliente_e_pedido(self):
        cliente = ClienteVirtual.objects.create(nome="Ana")
        categoria = Categoria.objects.create(nome="Doces")
        produto = Produto.objects.create(
            nome="Chocolate",
            codigo_barras="789400000001",
            preco_venda=Decimal("8.90"),
            foto="produtos/chocolate.jpg",
            categoria=categoria,
        )
        atendimento = AtendimentoVirtual.objects.create(
            cliente_virtual=cliente,
            horario_programado=timezone.now(),
            status=AtendimentoVirtual.Status.AGUARDANDO,
            valor_total=Decimal("0.00"),
        )
        pedido = PedidoVirtual.objects.create(
            atendimento=atendimento,
            produto=produto,
            quantidade=1,
        )

        self.assertEqual(pedido.atendimento, atendimento)
        self.assertEqual(pedido.produto, produto)
        self.assertEqual(atendimento.cliente_virtual, cliente)


class MotorClientesVirtuaisTest(TestCase):
    def test_garante_clientes_iniciais_sem_personalidade(self):
        garantir_clientes_iniciais()

        self.assertEqual(ClienteVirtual.objects.count(), 15)
        self.assertTrue(ClienteVirtual.objects.filter(nome="Ana", ativo=True).exists())

    def test_nao_gera_clientes_com_expediente_fechado(self):
        atendimentos = gerar_atendimentos_do_dia(timezone.now())

        self.assertEqual(atendimentos, [])
        self.assertEqual(AtendimentoVirtual.objects.count(), 0)

    def test_abertura_do_expediente_gera_atendimentos_do_dia(self):
        abrir_expediente()

        self.assertEqual(AtendimentoVirtual.objects.count(), 0)
        self.assertEqual(clientes_restantes_hoje(timezone.now()), 12)

    def test_cliente_chega_apos_intervalo_oculto(self):
        abrir_expediente()
        agora = timezone.now() + timedelta(minutes=9)

        resultado = processar_fluxo_clientes(agora)

        self.assertEqual(len(resultado["chegadas"]), 1)
        self.assertEqual(AtendimentoVirtual.objects.count(), 1)
        self.assertEqual(
            AtendimentoVirtual.objects.filter(
                status=AtendimentoVirtual.Status.AGUARDANDO
            ).count(),
            1,
        )

    def test_nao_gera_novo_cliente_enquanto_existe_cliente_aguardando(self):
        abrir_expediente()
        agora = timezone.now() + timedelta(minutes=9)
        processar_fluxo_clientes(agora)

        processar_fluxo_clientes(agora + timedelta(minutes=20))

        self.assertEqual(AtendimentoVirtual.objects.count(), 1)

    def test_fila_exibe_clientes_por_ordem_de_chegada_e_registra_evento(self):
        abrir_expediente()
        agora = timezone.now() + timedelta(minutes=9)
        processar_fluxo_clientes(agora)
        atendimento = AtendimentoVirtual.objects.get()

        fila = list(fila_ativa(agora))

        self.assertEqual(fila, [atendimento])
        self.assertTrue(
            EventoCliente.objects.filter(
                atendimento=atendimento,
                tipo=EventoCliente.Tipo.ENTROU_FILA,
            ).exists()
        )

    def test_desistencia_remove_cliente_da_fila_ativa_e_registra_evento(self):
        abrir_expediente()
        agora = timezone.now() + timedelta(minutes=9)
        processar_fluxo_clientes(agora)
        atendimento = AtendimentoVirtual.objects.get()
        atendimento.horario_programado = agora - timedelta(minutes=20)
        atendimento.save(update_fields=["horario_programado", "atualizado_em"])

        eventos = processar_desistencias(agora)
        atendimento.refresh_from_db()

        self.assertEqual(atendimento.status, AtendimentoVirtual.Status.DESISTIU)
        self.assertEqual(len(eventos), 1)
        self.assertFalse(fila_ativa(agora).filter(pk=atendimento.pk).exists())
        self.assertTrue(
            EventoCliente.objects.filter(
                atendimento=atendimento,
                tipo=EventoCliente.Tipo.DESISTIU,
            ).exists()
        )

    def test_fechar_expediente_para_processamento_do_motor(self):
        abrir_expediente()
        fechar_expediente()

        resultado = processar_fluxo_clientes(timezone.now())

        self.assertEqual(resultado, {"chegadas": [], "desistencias": []})


class CentralAtendimentoTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Alimentos")
        self.produto = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789500000001",
            preco_venda=Decimal("12.50"),
            foto="produtos/arroz.jpg",
            categoria=self.categoria,
        )
        registrar_entrada_estoque(self.produto, 3, "Entrada inicial")
        abrir_expediente()
        self.agora = timezone.now() + timedelta(minutes=9)
        processar_fluxo_clientes(self.agora)

    def test_iniciar_atendimento_vincula_venda_virtual(self):
        atendimento = AtendimentoVirtual.objects.order_by("horario_programado", "id").first()

        atendimento = iniciar_atendimento(atendimento.pk, self.agora)
        atendimento.refresh_from_db()

        self.assertEqual(atendimento.status, AtendimentoVirtual.Status.EM_ATENDIMENTO)
        self.assertIsNotNone(atendimento.horario_inicio)
        self.assertIsNotNone(atendimento.venda)
        self.assertEqual(atendimento.venda.tipo_cliente, Venda.TipoCliente.VIRTUAL)
        self.assertEqual(atendimento.venda.status, Venda.Status.EM_ANDAMENTO)
        self.assertEqual(atendimento_em_andamento(), atendimento)

    def test_nao_permite_dois_atendimentos_simultaneos(self):
        primeiro = AtendimentoVirtual.objects.get()
        segundo = AtendimentoVirtual.objects.create(
            cliente_virtual=ClienteVirtual.objects.exclude(pk=primeiro.cliente_virtual_id).first(),
            horario_programado=self.agora,
            status=AtendimentoVirtual.Status.AGUARDANDO,
            valor_total=Decimal("0.00"),
        )
        iniciar_atendimento(primeiro.pk, self.agora)

        with self.assertRaises(ValidationError):
            iniciar_atendimento(segundo.pk, self.agora)

    def test_finalizar_venda_finaliza_atendimento_e_mantem_integridade(self):
        atendimento = iniciar_atendimento(AtendimentoVirtual.objects.first().pk, self.agora)
        adicionar_produto_por_codigo(atendimento.venda, self.produto.codigo_barras)

        venda = finalizar_venda(atendimento.venda)
        finalizar_atendimento_por_venda(venda, self.agora)
        atendimento.refresh_from_db()
        self.produto.estoque.refresh_from_db()

        self.assertEqual(atendimento.status, AtendimentoVirtual.Status.FINALIZADO)
        self.assertEqual(atendimento.valor_total, Decimal("12.50"))
        self.assertEqual(self.produto.estoque.quantidade_atual, 2)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("12.50"))

    def test_cancelar_atendimento_cancela_venda_sem_movimentar_caixa_ou_estoque(self):
        atendimento = iniciar_atendimento(AtendimentoVirtual.objects.first().pk, self.agora)
        adicionar_produto_por_codigo(atendimento.venda, self.produto.codigo_barras)

        cancelar_atendimento(atendimento, self.agora)
        atendimento.refresh_from_db()
        atendimento.venda.refresh_from_db()
        self.produto.estoque.refresh_from_db()

        self.assertEqual(atendimento.status, AtendimentoVirtual.Status.DESISTIU)
        self.assertEqual(atendimento.venda.status, Venda.Status.CANCELADA)
        self.assertEqual(self.produto.estoque.quantidade_atual, 3)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("0.00"))

    def test_view_iniciar_redireciona_para_venda(self):
        atendimento = AtendimentoVirtual.objects.first()
        atendimento.horario_programado = timezone.now() - timedelta(minutes=1)
        atendimento.save(update_fields=["horario_programado", "atualizado_em"])

        response = self.client.post(reverse("clientes:iniciar", args=[atendimento.pk]))
        atendimento.refresh_from_db()

        self.assertRedirects(
            response,
            reverse("vendas:atendimento", args=[atendimento.venda.pk]),
        )
        self.assertEqual(atendimento.status, AtendimentoVirtual.Status.EM_ATENDIMENTO)


class ConversaGuiadaTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Alimentos")
        self.arroz = Produto.objects.create(
            nome="Arroz",
            codigo_barras="789600000001",
            preco_venda=Decimal("10.00"),
            foto="produtos/arroz.jpg",
            categoria=self.categoria,
        )
        self.feijao = Produto.objects.create(
            nome="Feijao",
            codigo_barras="789600000002",
            preco_venda=Decimal("8.00"),
            foto="produtos/feijao.jpg",
            categoria=self.categoria,
        )
        registrar_entrada_estoque(self.arroz, 2, "Entrada inicial")
        registrar_entrada_estoque(self.feijao, 2, "Entrada inicial")
        abrir_expediente()
        self.agora = timezone.now() + timedelta(minutes=9)
        processar_fluxo_clientes(self.agora)
        self.atendimento = AtendimentoVirtual.objects.get()
        self.atendimento.horario_programado = self.agora - timedelta(minutes=1)
        self.atendimento.save(update_fields=["horario_programado", "atualizado_em"])
        self.atendimento = iniciar_atendimento(self.atendimento.pk, self.agora)

    def test_iniciar_conversa_com_cliente_ativo(self):
        conversa = contexto_conversa(self.atendimento)
        self.atendimento.refresh_from_db()

        self.assertEqual(
            self.atendimento.estado_conversa,
            AtendimentoVirtual.EstadoConversa.EM_NEGOCIACAO,
        )
        self.assertIsNotNone(conversa["pedido"])
        self.assertTrue(
            InteracaoConversa.objects.filter(
                atendimento=self.atendimento,
                origem=InteracaoConversa.Origem.SISTEMA,
            ).exists()
        )

    def test_responder_sim_adiciona_produto_na_venda(self):
        responder_conversa(
            self.atendimento.pk,
            InteracaoConversa.Acao.SIM_TEMOS,
            self.agora,
        )
        self.atendimento.refresh_from_db()
        self.atendimento.venda.refresh_from_db()

        self.assertEqual(
            self.atendimento.estado_conversa,
            AtendimentoVirtual.EstadoConversa.ADICIONANDO_PRODUTOS,
        )
        self.assertEqual(self.atendimento.venda.itens.count(), 1)
        self.assertEqual(self.atendimento.venda.valor_total, Decimal("10.00"))

    def test_responder_nao_rejeita_pedido_e_encerra_sem_venda(self):
        responder_conversa(
            self.atendimento.pk,
            InteracaoConversa.Acao.NAO_TEMOS,
            self.agora,
        )
        self.atendimento.refresh_from_db()
        self.atendimento.venda.refresh_from_db()

        self.assertEqual(self.atendimento.status, AtendimentoVirtual.Status.FINALIZADO)
        self.assertEqual(
            self.atendimento.estado_conversa,
            AtendimentoVirtual.EstadoConversa.CONCLUIDO,
        )
        self.assertEqual(self.atendimento.venda.status, Venda.Status.CANCELADA)
        self.assertEqual(obter_caixa().saldo_atual, Decimal("0.00"))

    def test_ver_outros_produtos_alterna_pedido(self):
        pedido_inicial = PedidoVirtual.objects.get(atendimento=self.atendimento)

        responder_conversa(
            self.atendimento.pk,
            InteracaoConversa.Acao.VER_OUTROS_PRODUTOS,
            self.agora,
        )
        pedido_inicial.refresh_from_db()

        self.assertEqual(pedido_inicial.produto, self.feijao)
        self.assertEqual(
            self.atendimento.interacoes.filter(
                acao=InteracaoConversa.Acao.VER_OUTROS_PRODUTOS
            ).count(),
            1,
        )

    def test_finalizar_conversa_e_venda_corretamente(self):
        responder_conversa(
            self.atendimento.pk,
            InteracaoConversa.Acao.SIM_TEMOS,
            self.agora,
        )
        responder_conversa(
            self.atendimento.pk,
            InteracaoConversa.Acao.FINALIZAR_COMPRA,
            self.agora,
        )
        self.atendimento.refresh_from_db()

        self.assertEqual(
            self.atendimento.estado_conversa,
            AtendimentoVirtual.EstadoConversa.FINALIZANDO,
        )
        venda = finalizar_venda(self.atendimento.venda)
        finalizar_atendimento_por_venda(venda, self.agora)
        self.atendimento.refresh_from_db()

        self.assertEqual(self.atendimento.status, AtendimentoVirtual.Status.FINALIZADO)
        self.assertEqual(
            self.atendimento.estado_conversa,
            AtendimentoVirtual.EstadoConversa.CONCLUIDO,
        )
        self.assertEqual(obter_caixa().saldo_atual, Decimal("10.00"))

    def test_impede_resposta_fora_do_estado_atual(self):
        with self.assertRaises(ValidationError):
            responder_conversa(
                self.atendimento.pk,
                InteracaoConversa.Acao.FINALIZAR_COMPRA,
                self.agora,
            )
