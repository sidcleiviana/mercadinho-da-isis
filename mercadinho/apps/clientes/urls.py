from django.urls import path

from . import views

app_name = "clientes"

urlpatterns = [
    path("", views.fluxo_clientes, name="fluxo"),
    path("<int:pk>/iniciar/", views.iniciar, name="iniciar"),
    path("<int:pk>/cancelar/", views.cancelar, name="cancelar"),
    path("<int:pk>/conversa/", views.responder_conversa_view, name="responder_conversa"),
]
