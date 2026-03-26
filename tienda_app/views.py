from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Libro
from .services import CompraRapidaService
from .infra.factories import PaymentFactory

class CompraRapidaView(View):
    """
    Vista para compra rápida usando Factory Method y Builder
    """
    template_name = 'tienda_app/compra_rapida.html'
    
    def setup_service(self):
        """Factory Method: decide qué procesador usar según variable de entorno"""
        gateway = PaymentFactory.get_processor()
        return CompraRapidaService(procesador_pago=gateway)
    
    def get(self, request, libro_id):
        """Muestra el formulario de compra"""
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19  # Calculo estimado con IVA
        return render(request, self.template_name, {
            'libro': libro,
            'total': total
        })
    
    def post(self, request, libro_id):
        """Procesa la compra usando el servicio y builder"""
        try:
            # Obtener el servicio desde la fábrica
            servicio = self.setup_service()
            
            # Obtener o crear usuario anónimo si no está autenticado
            if request.user.is_authenticated:
                usuario = request.user
            else:
                # Crear o obtener un usuario genérico para compras anónimas
                usuario, created = User.objects.get_or_create(
                    username="anonimo_compra",
                    defaults={
                        "email": "anonimo@example.com",
                        "first_name": "Anonimo",
                        "last_name": "Compra"
                    }
                )
            
            # Obtener dirección del POST o usar valor por defecto
            direccion = request.POST.get('direccion', '').strip()
            if not direccion:
                direccion = "Retiro en tienda"
            
            # Procesar la compra
            total_pagado, orden_id = servicio.procesar(
                libro_id=libro_id,
                usuario=usuario,  # Pasamos el objeto User, no el ID
                direccion=direccion
            )
            
            if total_pagado:
                return HttpResponse(
                    f"✅ ¡Compra exitosa! Orden #{orden_id} - Total: ${total_pagado}"
                )
            else:
                return HttpResponse(
                    "❌ Error en el procesamiento del pago", 
                    status=500
                )
                
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()  # Esto mostrará el error completo en la terminal
            return HttpResponse(
                f"❌ Error inesperado: {str(e)}", 
                status=500
            )


# Vista opcional para la página de inicio
def index(request):
    """Vista simple para la raíz del sitio"""
    return HttpResponse("""
        <html>
        <head><title>Tienda</title></head>
        <body>
            <h1>Bienvenido a la Tienda</h1>
            <p>Para hacer una compra, ve a:</p>
            <ul>
                <li><a href="/compra/2/">/compra/2/</a> (Libro Clean Code)</li>
            </ul>
        </body>
        </html>
    """)