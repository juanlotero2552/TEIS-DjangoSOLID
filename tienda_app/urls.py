from django.urls import path
from .views import CompraRapidaView, index
from .api.views import CompraAPIView, LibroListAPIView

urlpatterns = [
    # Vistas HTML (Tutorial 1 y 2)
    path('', index, name='index'),
    path('compra/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida'),
    
    # API REST (Tutorial 3)
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    path('api/v1/libros/', LibroListAPIView.as_view(), name='api_libros'),
]
