from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("expediente/abrir/", views.abrir, name="abrir_expediente"),
    path("expediente/fechar/", views.fechar, name="fechar_expediente"),
]
