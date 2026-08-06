from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import MovimentacaoFinanceiraForm
from .models import MovimentacaoFinanceira
from .services import obter_caixa, registrar_movimentacao_financeira


class CaixaDashboardView(View):
    template_name = "caixa/caixa_dashboard.html"

    def get(self, request):
        caixa = obter_caixa()
        movimentacoes = MovimentacaoFinanceira.objects.select_related("venda").order_by(
            "-data", "-id"
        )
        entradas = movimentacoes.filter(tipo=MovimentacaoFinanceira.Tipo.ENTRADA)
        saidas = movimentacoes.filter(tipo=MovimentacaoFinanceira.Tipo.SAIDA)
        return render(
            request,
            self.template_name,
            {
                "caixa": caixa,
                "entradas": entradas[:10],
                "saidas": saidas[:10],
                "movimentacoes": movimentacoes[:30],
            },
        )


class RegistrarMovimentacaoView(View):
    template_name = "caixa/movimentacao_form.html"
    tipo = None
    titulo = ""

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"form": MovimentacaoFinanceiraForm(), "titulo": self.titulo},
        )

    def post(self, request):
        form = MovimentacaoFinanceiraForm(request.POST)
        if form.is_valid():
            try:
                registrar_movimentacao_financeira(
                    tipo=self.tipo,
                    valor=form.cleaned_data["valor"],
                    descricao=form.cleaned_data["descricao"],
                )
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                messages.success(request, "Movimentacao financeira registrada.")
                return redirect(reverse("caixa:dashboard"))

        return render(
            request,
            self.template_name,
            {"form": form, "titulo": self.titulo},
        )


class EntradaFinanceiraView(RegistrarMovimentacaoView):
    tipo = MovimentacaoFinanceira.Tipo.ENTRADA
    titulo = "Registrar Entrada"


class SaidaFinanceiraView(RegistrarMovimentacaoView):
    tipo = MovimentacaoFinanceira.Tipo.SAIDA
    titulo = "Registrar Saida"
