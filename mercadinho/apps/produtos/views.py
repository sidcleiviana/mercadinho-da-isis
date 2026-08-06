from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ProdutoForm
from .models import Produto


class ProdutoListView(ListView):
    model = Produto
    template_name = "produtos/produto_lista.html"
    context_object_name = "produtos"
    paginate_by = 12

    def get_queryset(self):
        queryset = Produto.objects.select_related("categoria").order_by("nome")
        termo = self.request.GET.get("q", "").strip()
        if termo:
            queryset = queryset.filter(
                Q(nome__icontains=termo) | Q(codigo_barras__icontains=termo)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["termo_busca"] = self.request.GET.get("q", "").strip()
        return context


class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/produto_form.html"
    success_url = reverse_lazy("produtos:lista")

    def form_valid(self, form):
        messages.success(self.request, "Produto salvo com sucesso.")
        return super().form_valid(form)


class ProdutoUpdateView(UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/produto_form.html"
    success_url = reverse_lazy("produtos:lista")

    def get_queryset(self):
        return Produto.objects.select_related("categoria")

    def form_valid(self, form):
        messages.success(self.request, "Produto atualizado com sucesso.")
        return super().form_valid(form)


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = "produtos/produto_detalhe.html"
    context_object_name = "produto"

    def get_queryset(self):
        return Produto.objects.select_related("categoria")
