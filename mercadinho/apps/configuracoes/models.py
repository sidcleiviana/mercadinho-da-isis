from django.db import models

from apps.core.models import ModeloBase


class Configuracao(ModeloBase):
    nome_mercado = models.CharField(max_length=160)
    quantidade_maxima_clientes_virtuais_por_dia = models.PositiveIntegerField()
    tempo_maximo_espera = models.PositiveIntegerField()
    horario_abertura = models.TimeField()
    horario_fechamento = models.TimeField()

    class Meta:
        verbose_name = "Configuracao"
        verbose_name_plural = "Configuracoes"

    def __str__(self):
        return self.nome_mercado
