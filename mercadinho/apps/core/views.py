from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.caixa.services import obter_caixa
from apps.estoque.models import Estoque
from apps.produtos.models import Produto
from apps.vendas.models import Venda
from apps.clientes.services import eventos_recentes, fila_ativa, processar_fluxo_clientes

from .models import Expediente
from .services import abrir_expediente, fechar_expediente, obter_expediente

def dashboard(request):
    expediente = obter_expediente()
    processar_fluxo_clientes()
    caixa = obter_caixa()
    produtos_ativos = Produto.objects.filter(ativo=True).count()
    total_estoque = (
        Estoque.objects.aggregate(total=Sum("quantidade_atual"))["total"] or 0
    )
    ultima_venda = (
        Venda.objects.filter(status=Venda.Status.CONCLUIDA)
        .order_by("-data", "-id")
        .first()
    )
    notificacoes = []
    if expediente.status == Expediente.Status.ABERTO:
        notificacoes.append("Expediente aberto.")
    else:
        notificacoes.append("Expediente fechado.")
    if produtos_ativos == 0:
        notificacoes.append("Nenhum produto ativo cadastrado.")
    if total_estoque == 0:
        notificacoes.append("Nenhum produto em estoque.")
    if ultima_venda:
        notificacoes.append(f"Ultima venda: {ultima_venda.numero_venda}.")
    fila_clientes = fila_ativa()

    return render(
        request,
        "core/dashboard.html",
        {
            "expediente": expediente,
            "caixa": caixa,
            "produtos_ativos": produtos_ativos,
            "total_estoque": total_estoque,
            "ultima_venda": ultima_venda,
            "notificacoes": notificacoes,
            "clientes_aguardando": fila_clientes.count(),
            "eventos_clientes": eventos_recentes(5),
        },
    )


@require_POST
def abrir(request):
    abrir_expediente()
    messages.success(request, "Expediente aberto.")
    return redirect(reverse("core:dashboard"))


@require_POST
def fechar(request):
    fechar_expediente()
    messages.success(request, "Expediente fechado.")
    return redirect(reverse("core:dashboard"))
