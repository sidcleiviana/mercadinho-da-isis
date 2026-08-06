from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import ModeloBase
from apps.vendas.models import Venda


class Caixa(ModeloBase):
    saldo_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if (
            self.pk
            and Caixa.objects.filter(pk=self.pk).exists()
            and not getattr(self, "_permitir_atualizar_saldo", False)
        ):
            saldo_original = Caixa.objects.get(pk=self.pk).saldo_atual
            if self.saldo_atual != saldo_original:
                raise ValidationError(
                    "O saldo do caixa deve ser alterado apenas por movimentacoes."
                )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Caixa"
        verbose_name_plural = "Caixas"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(id=1),
                name="caixa_unico_id_igual_1",
            ),
            models.CheckConstraint(
                condition=models.Q(saldo_atual__gte=0),
                name="caixa_saldo_atual_nao_negativo",
            ),
        ]

    def __str__(self):
        return f"Caixa - R$ {self.saldo_atual}"


class MovimentacaoFinanceira(ModeloBase):
    class Tipo(models.TextChoices):
        ENTRADA = "entrada", "Entrada"
        SAIDA = "saida", "Saida"

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255)
    data = models.DateTimeField()
    venda = models.ForeignKey(
        Venda,
        on_delete=models.PROTECT,
        related_name="movimentacoes_financeiras",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-data", "-id"]
        verbose_name = "Movimentacao Financeira"
        verbose_name_plural = "Movimentacoes Financeiras"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(valor__gte=0),
                name="movimentacao_financeira_valor_nao_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} - R$ {self.valor}"
