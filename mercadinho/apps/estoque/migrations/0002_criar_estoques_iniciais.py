from django.db import migrations


def criar_estoques_iniciais(apps, schema_editor):
    Produto = apps.get_model("produtos", "Produto")
    Estoque = apps.get_model("estoque", "Estoque")

    produtos_sem_estoque = Produto.objects.filter(estoque__isnull=True)
    for produto in produtos_sem_estoque:
        Estoque.objects.get_or_create(
            produto=produto,
            defaults={"quantidade_atual": 0},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0001_initial"),
        ("produtos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(criar_estoques_iniciais, migrations.RunPython.noop),
    ]
