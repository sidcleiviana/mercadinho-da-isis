from django.db import models

from apps.core.models import ModeloBase
from apps.produtos.models import Produto


class Venda(ModeloBase):
    class TipoCliente(models.TextChoices):
        REAL = "real", "Real"
        VIRTUAL = "virtual", "Virtual"

    class Status(models.TextChoices):
        EM_ANDAMENTO = "em_andamento", "Em Andamento"
        CONCLUIDA = "concluida", "Concluida"
        CANCELADA = "cancelada", "Cancelada"

    numero_venda = models.CharField(max_length=40, unique=True)
    data = models.DateTimeField()
    tipo_cliente = models.CharField(max_length=10, choices=TipoCliente.choices)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices)

    class Meta:
        ordering = ["-data", "-id"]
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(valor_total__gte=0),
                name="venda_valor_total_nao_negativo",
            ),
        ]

    def __str__(self):
        return f"Venda {self.numero_venda}"


class ItemVenda(ModeloBase):
    venda = models.ForeignKey(
        Venda,
        on_delete=models.PROTECT,
        related_name="itens",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="itens_venda",
    )
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["id"]
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(valor_unitario__gte=0),
                name="item_venda_valor_unitario_nao_negativo",
            ),
            models.CheckConstraint(
                condition=models.Q(valor_total__gte=0),
                name="item_venda_valor_total_nao_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.produto} x {self.quantidade}"
