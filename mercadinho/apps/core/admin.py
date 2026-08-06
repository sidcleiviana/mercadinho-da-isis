from django.contrib import admin

from .models import Expediente


@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "aberto_em", "fechado_em", "atualizado_em"]
    readonly_fields = ["criado_em", "atualizado_em"]
