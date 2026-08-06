from django.contrib import admin

from .models import (
    AtendimentoVirtual,
    ClienteVirtual,
    EventoCliente,
    InteracaoConversa,
    PedidoVirtual,
)


@admin.register(ClienteVirtual)
class ClienteVirtualAdmin(admin.ModelAdmin):
    list_display = ["nome", "ativo"]
    search_fields = ["nome"]
    list_filter = ["ativo"]


@admin.register(AtendimentoVirtual)
class AtendimentoVirtualAdmin(admin.ModelAdmin):
    list_display = [
        "cliente_virtual",
        "horario_programado",
        "horario_inicio",
        "horario_finalizacao",
        "status",
        "estado_conversa",
        "valor_total",
    ]
    list_filter = ["status", "estado_conversa"]
    search_fields = ["cliente_virtual__nome"]
    list_select_related = ["cliente_virtual", "venda"]


@admin.register(PedidoVirtual)
class PedidoVirtualAdmin(admin.ModelAdmin):
    list_display = ["atendimento", "produto", "quantidade"]
    list_select_related = ["atendimento", "produto"]


@admin.register(EventoCliente)
class EventoClienteAdmin(admin.ModelAdmin):
    list_display = ["tipo", "mensagem", "data", "atendimento"]
    list_filter = ["tipo"]
    search_fields = ["mensagem", "atendimento__cliente_virtual__nome"]
    list_select_related = ["atendimento", "atendimento__cliente_virtual"]


@admin.register(InteracaoConversa)
class InteracaoConversaAdmin(admin.ModelAdmin):
    list_display = ["atendimento", "origem", "acao", "mensagem", "data"]
    list_filter = ["origem", "acao"]
    search_fields = ["mensagem", "atendimento__cliente_virtual__nome"]
    list_select_related = ["atendimento", "atendimento__cliente_virtual"]
