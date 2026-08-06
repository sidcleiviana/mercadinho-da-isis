from django.urls import path

from . import views

app_name = "vendas"

urlpatterns = [
    path("", views.VendaListView.as_view(), name="lista"),
    path("nova/", views.nova_venda, name="nova"),
    path("<int:pk>/", views.VendaAtendimentoView.as_view(), name="atendimento"),
    path("<int:pk>/adicionar/", views.adicionar_item, name="adicionar_item"),
    path("<int:pk>/finalizar/", views.finalizar, name="finalizar"),
    path("<int:pk>/cancelar/", views.cancelar, name="cancelar"),
]
