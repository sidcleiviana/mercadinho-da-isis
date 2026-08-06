from django.contrib import admin

from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome", "cor", "ordem_exibicao", "criado_em", "atualizado_em"]
    search_fields = ["nome"]
    ordering = ["ordem_exibicao", "nome"]


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["nome", "codigo_barras", "categoria", "preco_venda", "ativo"]
    list_filter = ["ativo", "categoria"]
    search_fields = ["nome", "codigo_barras"]
    list_select_related = ["categoria"]
