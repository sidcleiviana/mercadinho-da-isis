from datetime import time
from decimal import Decimal

from django.db.models import Count, ExpressionWrapper, F, Sum
from django.db.models.fields import DurationField
from django.utils import timezone

from apps.caixa.models import MovimentacaoFinanceira
from apps.caixa.services import obter_caixa
from apps.clientes.models import AtendimentoVirtual, EventoCliente
from apps.estoque.models import Estoque, MovimentacaoEstoque
from apps.vendas.models import ItemVenda, Venda


ESTOQUE_BAIXO_LIMITE = 3


def intervalo_do_dia(referencia=None):
    referencia = referencia or timezone.localtime()
    inicio = timezone.make_aware(
        timezone.datetime.combine(referencia.date(), time.min),
        timezone.get_current_timezone(),
    )
    fim = timezone.make_aware(
        timezone.datetime.combine(referencia.date(), time.max),
        timezone.get_current_timezone(),
    )
    return inicio, fim


def relatorio_vendas(inicio=None, fim=None):
    inicio, fim = (inicio, fim) if inicio and fim else intervalo_do_dia()
    vendas = Venda.objects.filter(
        status=Venda.Status.CONCLUIDA,
        data__range=(inicio, fim),
    )
    resumo = vendas.aggregate(
        total_vendas=Count("id"),
        valor_total=Sum("valor_total"),
    )
    produtos_mais_vendidos = (
        ItemVenda.objects.filter(venda__in=vendas)
        .values("produto__nome")
        .annotate(
            quantidade_total=Sum("quantidade"),
            valor_total=Sum("valor_total"),
        )
        .order_by("-quantidade_total", "produto__nome")[:10]
    )
    return {
        "inicio": inicio,
        "fim": fim,
        "total_vendas": resumo["total_vendas"] or 0,
        "valor_total": resumo["valor_total"] or Decimal("0.00"),
        "produtos_mais_vendidos": produtos_mais_vendidos,
        "vendas": vendas.order_by("-data", "-id")[:20],
    }


def relatorio_caixa(inicio=None, fim=None):
    inicio, fim = (inicio, fim) if inicio and fim else intervalo_do_dia()
    movimentacoes = MovimentacaoFinanceira.objects.filter(data__range=(inicio, fim))
    entradas = movimentacoes.filter(tipo=MovimentacaoFinanceira.Tipo.ENTRADA)
    saidas = movimentacoes.filter(tipo=MovimentacaoFinanceira.Tipo.SAIDA)
    return {
        "inicio": inicio,
        "fim": fim,
        "saldo_atual": obter_caixa().saldo_atual,
        "total_entradas": entradas.aggregate(total=Sum("valor"))["total"]
        or Decimal("0.00"),
        "total_saidas": saidas.aggregate(total=Sum("valor"))["total"]
        or Decimal("0.00"),
        "movimentacoes_recentes": MovimentacaoFinanceira.objects.select_related(
            "venda"
        ).order_by("-data", "-id")[:20],
        "movimentacoes_do_dia": movimentacoes.order_by("-data", "-id")[:20],
    }


def relatorio_estoque(inicio=None, fim=None):
    inicio, fim = (inicio, fim) if inicio and fim else intervalo_do_dia()
    saidas = MovimentacaoEstoque.objects.filter(
        tipo=MovimentacaoEstoque.Tipo.VENDA,
        data__range=(inicio, fim),
    )
    produtos_maior_saida = (
        saidas.values("produto__nome")
        .annotate(quantidade_total=Sum("quantidade"))
        .order_by("-quantidade_total", "produto__nome")[:10]
    )
    produtos_estoque_baixo = Estoque.objects.select_related("produto").filter(
        quantidade_atual__lte=ESTOQUE_BAIXO_LIMITE
    )
    produtos_sem_movimentacao = (
        Estoque.objects.select_related("produto")
        .exclude(produto__movimentacoes_estoque__data__range=(inicio, fim))
        .order_by("produto__nome")[:20]
    )
    return {
        "inicio": inicio,
        "fim": fim,
        "quantidade_total_estoque": Estoque.objects.aggregate(
            total=Sum("quantidade_atual")
        )["total"]
        or 0,
        "produtos_maior_saida": produtos_maior_saida,
        "produtos_estoque_baixo": produtos_estoque_baixo.order_by(
            "quantidade_atual", "produto__nome"
        )[:20],
        "produtos_sem_movimentacao": produtos_sem_movimentacao,
        "limite_estoque_baixo": ESTOQUE_BAIXO_LIMITE,
    }


def relatorio_clientes(inicio=None, fim=None):
    inicio, fim = (inicio, fim) if inicio and fim else intervalo_do_dia()
    atendimentos = AtendimentoVirtual.objects.filter(
        horario_programado__range=(inicio, fim)
    )
    atendidos = atendimentos.filter(status=AtendimentoVirtual.Status.FINALIZADO)
    desistentes = atendimentos.filter(status=AtendimentoVirtual.Status.DESISTIU)
    duracao = ExpressionWrapper(
        F("horario_finalizacao") - F("horario_inicio"),
        output_field=DurationField(),
    )
    atendimentos_com_duracao = atendidos.exclude(
        horario_inicio__isnull=True,
    ).exclude(
        horario_finalizacao__isnull=True,
    ).annotate(duracao=duracao)
    duracoes = [item.duracao for item in atendimentos_com_duracao if item.duracao]
    tempo_medio = None
    if duracoes:
        tempo_medio = sum(duracoes, duracoes[0] - duracoes[0]) / len(duracoes)
    return {
        "inicio": inicio,
        "fim": fim,
        "clientes_atendidos": atendidos.count(),
        "clientes_desistentes": desistentes.count(),
        "tempo_medio_atendimento": tempo_medio,
        "fluxo_clientes": atendimentos.select_related("cliente_virtual").order_by(
            "horario_programado", "id"
        ),
        "eventos_relevantes": EventoCliente.objects.filter(
            data__range=(inicio, fim)
        ).select_related("atendimento", "atendimento__cliente_virtual")[:20],
    }


def relatorio_geral():
    vendas = relatorio_vendas()
    caixa = relatorio_caixa()
    estoque = relatorio_estoque()
    clientes = relatorio_clientes()
    return {
        "vendas": vendas,
        "caixa": caixa,
        "estoque": estoque,
        "clientes": clientes,
        "eventos_relevantes": EventoCliente.objects.select_related(
            "atendimento", "atendimento__cliente_virtual"
        ).order_by("-data", "-id")[:10],
    }
