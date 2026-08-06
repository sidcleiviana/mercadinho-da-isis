from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.core.services import obter_expediente

from .models import AtendimentoVirtual
from .services import (
    atendimento_em_andamento,
    cancelar_atendimento,
    atendimentos_do_dia,
    clientes_previstos_hoje,
    clientes_restantes_hoje,
    eventos_recentes,
    fila_ativa,
    iniciar_atendimento,
    processar_fluxo_clientes,
    responder_conversa,
)


def fluxo_clientes(request):
    agora = timezone.now()
    processar_fluxo_clientes(agora)
    atendimentos = atendimentos_do_dia(agora)
    atendidos = atendimentos.filter(status=AtendimentoVirtual.Status.FINALIZADO).count()
    desistentes = atendimentos.filter(status=AtendimentoVirtual.Status.DESISTIU).count()
    expediente = obter_expediente()
    tempo_expediente = None
    if expediente.aberto_em:
        fim = expediente.fechado_em or agora
        tempo_expediente = fim - expediente.aberto_em
    return render(
        request,
        "clientes/fluxo.html",
        {
            "expediente": expediente,
            "fila": fila_ativa(agora),
            "atendimento_atual": atendimento_em_andamento(),
            "clientes_previstos": clientes_previstos_hoje(),
            "clientes_restantes": clientes_restantes_hoje(agora),
            "clientes_atendidos": atendidos,
            "clientes_desistentes": desistentes,
            "tempo_expediente": tempo_expediente,
            "eventos": eventos_recentes(20),
            "agora": agora,
        },
    )


@require_POST
def iniciar(request, pk):
    atendimento = get_object_or_404(AtendimentoVirtual, pk=pk)
    try:
        atendimento = iniciar_atendimento(atendimento.pk)
    except ValidationError as exc:
        messages.error(request, exc.message)
        return redirect(reverse("clientes:fluxo"))

    messages.success(request, "Atendimento iniciado.")
    return redirect(reverse("vendas:atendimento", args=[atendimento.venda_id]))


@require_POST
def cancelar(request, pk):
    atendimento = get_object_or_404(AtendimentoVirtual, pk=pk)
    try:
        cancelar_atendimento(atendimento)
    except ValidationError as exc:
        messages.error(request, exc.message)
    else:
        messages.success(request, "Atendimento cancelado.")
    return redirect(reverse("clientes:fluxo"))


@require_POST
def responder_conversa_view(request, pk):
    acao = request.POST.get("acao", "")
    try:
        atendimento = responder_conversa(pk, acao)
    except ValidationError as exc:
        messages.error(request, exc.message)
        atendimento = get_object_or_404(AtendimentoVirtual, pk=pk)
    else:
        messages.success(request, "Resposta registrada.")

    if atendimento.venda_id and atendimento.status == AtendimentoVirtual.Status.EM_ATENDIMENTO:
        return redirect(reverse("vendas:atendimento", args=[atendimento.venda_id]))
    return redirect(reverse("clientes:fluxo"))
