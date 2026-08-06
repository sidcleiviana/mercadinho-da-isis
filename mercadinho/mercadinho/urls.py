from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clientes/", include("apps.clientes.urls")),
    path("vendas/", include("apps.vendas.urls")),
    path("caixa/", include("apps.caixa.urls")),
    path("estoque/", include("apps.estoque.urls")),
    path("produtos/", include("apps.produtos.urls")),
    path("relatorios/", include("apps.relatorios.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
