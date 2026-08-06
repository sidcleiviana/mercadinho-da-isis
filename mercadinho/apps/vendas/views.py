from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from apps.clientes.services import (
    cancelar_atendimento_por_venda,
    contexto_conversa,
    finalizar_atendimento_por_venda,
)

from .forms import CodigoBarrasForm
from .models import Venda
from .services import (
    adicionar_produto_por_codigo,
    cancelar_venda,
    finalizar_venda,
    iniciar_venda,
)


class VendaListView(ListView):
    model = Venda
    template_name = "vendas/venda_lista.html"
    context_object_name = "vendas"
    paginate_by = 20

    def get_queryset(self):
        return Venda.objects.prefetch_related("itens").order_by("-data", "-id")


def nova_venda(request):
    venda = iniciar_venda()
    return redirect(reverse("vendas:atendimento", args=[venda.pk]))


class VendaAtendimentoView(DetailView):
    model = Venda
    template_name = "vendas/venda_atendimento.html"
    context_object_name = "venda"

    def get_queryset(self):
        return Venda.objects.prefetch_related("itens__produto").select_related(
            "atendimento_virtual", "atendimento_virtual__cliente_virtual"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CodigoBarrasForm()
        atendimento = getattr(self.object, "atendimento_virtual", None)
        if atendimento and atendimento.status == atendimento.Status.EM_ATENDIMENTO:
            context["conversa"] = contexto_conversa(atendimento)
        return context


def adicionar_item(request, pk):
    venda = get_object_or_404(Venda, pk=pk, status=Venda.Status.EM_ANDAMENTO)
    form = CodigoBarrasForm(request.POST)
    if form.is_valid():
        try:
            adicionar_produto_por_codigo(venda, form.cleaned_data["codigo_barras"])
        except ValidationError as exc:
            messages.error(request, exc.message)
        else:
            messages.success(request, "Produto adicionado.")
    return redirect(reverse("vendas:atendimento", args=[venda.pk]))


def finalizar(request, pk):
    venda = get_object_or_404(Venda, pk=pk, status=Venda.Status.EM_ANDAMENTO)
    if request.method == "POST":
        try:
            venda = finalizar_venda(venda)
        except ValidationError as exc:
            messages.error(request, exc.message)
            return redirect(reverse("vendas:atendimento", args=[venda.pk]))
        atendimento = finalizar_atendimento_por_venda(venda)
        messages.success(request, "Venda concluida.")
        if atendimento:
            return redirect(reverse("clientes:fluxo"))
        return redirect(reverse("vendas:lista"))
    return render(request, "vendas/confirmar_finalizacao.html", {"venda": venda})


def cancelar(request, pk):
    venda = get_object_or_404(Venda, pk=pk, status=Venda.Status.EM_ANDAMENTO)
    if request.method == "POST":
        cancelar_venda(venda)
        atendimento = cancelar_atendimento_por_venda(venda)
        messages.success(request, "Venda cancelada.")
        if atendimento:
            return redirect(reverse("clientes:fluxo"))
        return redirect(reverse("vendas:lista"))
    return render(request, "vendas/confirmar_cancelamento.html", {"venda": venda})
