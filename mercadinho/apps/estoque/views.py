from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from apps.produtos.models import Produto

from .forms import EntradaEstoqueForm
from .models import Estoque, MovimentacaoEstoque
from .services import (
    garantir_estoque_para_produto,
    garantir_estoques_iniciais,
    registrar_entrada_estoque,
)


class EstoqueListView(ListView):
    model = Estoque
    template_name = "estoque/estoque_lista.html"
    context_object_name = "estoques"
    paginate_by = 12

    def get_queryset(self):
        garantir_estoques_iniciais()
        queryset = Estoque.objects.select_related("produto", "produto__categoria").order_by(
            "produto__nome"
        )
        termo = self.request.GET.get("q", "").strip()
        if termo:
            queryset = queryset.filter(
                Q(produto__nome__icontains=termo)
                | Q(produto__codigo_barras__icontains=termo)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["termo_busca"] = self.request.GET.get("q", "").strip()
        return context


class EntradaEstoqueView(View):
    template_name = "estoque/estoque_entrada.html"

    def get_produto(self):
        return get_object_or_404(
            Produto.objects.select_related("categoria"),
            pk=self.kwargs["produto_pk"],
        )

    def get(self, request, *args, **kwargs):
        produto = self.get_produto()
        estoque = garantir_estoque_para_produto(produto)
        return render(
            request,
            self.template_name,
            {"produto": produto, "estoque": estoque, "form": EntradaEstoqueForm()},
        )

    def post(self, request, *args, **kwargs):
        produto = self.get_produto()
        form = EntradaEstoqueForm(request.POST)
        if form.is_valid():
            registrar_entrada_estoque(
                produto=produto,
                quantidade=form.cleaned_data["quantidade"],
                observacao=form.cleaned_data["observacao"],
            )
            messages.success(request, "Estoque atualizado com sucesso.")
            return redirect(reverse("estoque:lista"))

        estoque = garantir_estoque_para_produto(produto)
        return render(
            request,
            self.template_name,
            {"produto": produto, "estoque": estoque, "form": form},
        )


class MovimentacaoEstoqueListView(ListView):
    model = MovimentacaoEstoque
    template_name = "estoque/movimentacao_lista.html"
    context_object_name = "movimentacoes"
    paginate_by = 20

    def get_queryset(self):
        queryset = MovimentacaoEstoque.objects.select_related(
            "produto", "produto__categoria"
        ).order_by("-data", "-id")
        termo = self.request.GET.get("q", "").strip()
        if termo:
            queryset = queryset.filter(
                Q(produto__nome__icontains=termo)
                | Q(produto__codigo_barras__icontains=termo)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["termo_busca"] = self.request.GET.get("q", "").strip()
        return context
