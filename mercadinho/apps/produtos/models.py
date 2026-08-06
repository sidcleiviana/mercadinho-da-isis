from django.db import models

from apps.core.models import ModeloBase


class Categoria(ModeloBase):
    nome = models.CharField(max_length=120, unique=True)
    cor = models.CharField(max_length=20, blank=True)
    ordem_exibicao = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem_exibicao", "nome"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Produto(ModeloBase):
    nome = models.CharField(max_length=160)
    codigo_barras = models.CharField(max_length=80, unique=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to="produtos/")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="produtos",
    )
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(preco_venda__gte=0),
                name="produto_preco_venda_nao_negativo",
            ),
        ]

    def __str__(self):
        return self.nome
