from django.contrib import admin

from .models import Estoque, MovimentacaoEstoque


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ["produto", "quantidade_atual", "atualizado_em"]
    search_fields = ["produto__nome", "produto__codigo_barras"]
    list_select_related = ["produto"]


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ["produto", "tipo", "quantidade", "data"]
    list_filter = ["tipo"]
    search_fields = ["produto__nome", "produto__codigo_barras", "observacao"]
    list_select_related = ["produto"]
