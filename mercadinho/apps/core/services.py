from django.utils import timezone

from .models import Expediente


def obter_expediente():
    expediente, _ = Expediente.objects.get_or_create(pk=1)
    return expediente


def abrir_expediente():
    expediente = obter_expediente()
    if expediente.status != Expediente.Status.ABERTO:
        expediente.status = Expediente.Status.ABERTO
        expediente.aberto_em = timezone.now()
        expediente.fechado_em = None
        expediente.save(update_fields=["status", "aberto_em", "fechado_em", "atualizado_em"])
        from apps.clientes.services import gerar_atendimentos_do_dia

        gerar_atendimentos_do_dia(expediente.aberto_em)
    return expediente


def fechar_expediente():
    expediente = obter_expediente()
    if expediente.status != Expediente.Status.FECHADO:
        expediente.status = Expediente.Status.FECHADO
        expediente.fechado_em = timezone.now()
        expediente.save(update_fields=["status", "fechado_em", "atualizado_em"])
    return expediente
