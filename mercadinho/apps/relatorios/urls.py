from django.urls import path

from . import views

app_name = "relatorios"

urlpatterns = [
    path("", views.resumo, name="resumo"),
    path("vendas/", views.vendas, name="vendas"),
    path("caixa/", views.caixa, name="caixa"),
    path("estoque/", views.estoque, name="estoque"),
    path("clientes/", views.clientes, name="clientes"),
]
