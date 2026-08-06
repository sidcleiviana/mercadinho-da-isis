from django.contrib import admin

from .models import ItemVenda, Venda


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 0
    readonly_fields = ["produto", "quantidade", "valor_unitario", "valor_total"]
    can_delete = False


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ["numero_venda", "data", "tipo_cliente", "valor_total", "status"]
    list_filter = ["status", "tipo_cliente"]
    search_fields = ["numero_venda"]
    inlines = [ItemVendaInline]


@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ["venda", "produto", "quantidade", "valor_unitario", "valor_total"]
    search_fields = ["venda__numero_venda", "produto__nome", "produto__codigo_barras"]
    list_select_related = ["venda", "produto"]
