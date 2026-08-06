from django.contrib import admin

from .models import Caixa, MovimentacaoFinanceira


@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ["id", "saldo_atual", "atualizado_em"]
    readonly_fields = ["saldo_atual", "criado_em", "atualizado_em"]


@admin.register(MovimentacaoFinanceira)
class MovimentacaoFinanceiraAdmin(admin.ModelAdmin):
    list_display = ["tipo", "valor", "descricao", "data", "venda"]
    list_filter = ["tipo"]
    search_fields = ["descricao"]
    readonly_fields = ["criado_em", "atualizado_em"]
