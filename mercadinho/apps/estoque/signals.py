from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.produtos.models import Produto

from .models import Estoque


@receiver(post_save, sender=Produto)
def criar_estoque_inicial(sender, instance, created, **kwargs):
    if created:
        Estoque.objects.get_or_create(
            produto=instance,
            defaults={"quantidade_atual": 0},
        )
