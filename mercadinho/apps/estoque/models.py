from django.db import models

from apps.core.models import ModeloBase
from apps.produtos.models import Produto


class Estoque(ModeloBase):
    produto = models.OneToOneField(
        Produto,
        on_delete=models.PROTECT,
        related_name="estoque",
    )
    quantidade_atual = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["produto__nome"]
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

    def __str__(self):
        return f"{self.produto} - {self.quantidade_atual}"


class MovimentacaoEstoque(ModeloBase):
    class Tipo(models.TextChoices):
        ENTRADA = "entrada", "Entrada"
        VENDA = "venda", "Venda"
        AJUSTE_MANUAL = "ajuste_manual", "Ajuste Manual"

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="movimentacoes_estoque",
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField()
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ["-data", "-id"]
        verbose_name = "Movimentacao de Estoque"
        verbose_name_plural = "Movimentacoes de Estoque"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto} - {self.quantidade}"
