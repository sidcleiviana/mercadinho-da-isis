from django.urls import path

from . import views

app_name = "caixa"

urlpatterns = [
    path("", views.CaixaDashboardView.as_view(), name="dashboard"),
    path("entrada/", views.EntradaFinanceiraView.as_view(), name="entrada"),
    path("saida/", views.SaidaFinanceiraView.as_view(), name="saida"),
]
