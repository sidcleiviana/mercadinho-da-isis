from django.urls import path

from . import views

app_name = "estoque"

urlpatterns = [
    path("", views.EstoqueListView.as_view(), name="lista"),
    path("historico/", views.MovimentacaoEstoqueListView.as_view(), name="historico"),
    path("<int:produto_pk>/entrada/", views.EntradaEstoqueView.as_view(), name="entrada"),
]
