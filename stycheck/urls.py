from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Redirige la página principal vacía a /servicios/
    path('', RedirectView.as_view(url='servicios/', permanent=True)),

    path('admin/', admin.site.urls),
    path('servicios/', include('servicios.urls')),  # O como tengas configurada tu app
    path('citas/', include('citas.urls')),
    path('api/', include('stycheck.api_urls')),
]
