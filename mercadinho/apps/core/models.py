from django.db import models


class ModeloBase(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Expediente(ModeloBase):
    class Status(models.TextChoices):
        ABERTO = "aberto", "Aberto"
        FECHADO = "fechado", "Fechado"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.FECHADO,
    )
    aberto_em = models.DateTimeField(null=True, blank=True)
    fechado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(id=1),
                name="expediente_unico_id_igual_1",
            ),
        ]

    def __str__(self):
        return self.get_status_display()
