from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenInputSerializer, LibroSerializer
from tienda_app.services import CompraRapidaService
from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Libro
from django.contrib.auth.models import User

class CompraAPIView(APIView):
    """
    Endpoint para procesar compras vía JSON.
    POST /api/v1/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123"}
    """
    
    def post(self, request):
        # 1. Validación de datos de entrada
        serializer = OrdenInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        datos = serializer.validated_data
        
        try:
            # 2. Inyección de Dependencias (Factory)
            gateway = PaymentFactory.get_processor()
            
            # 3. Ejecución de Lógica de Negocio
            servicio = CompraRapidaService(procesador_pago=gateway)
            
            # Manejar usuario anónimo
            if request.user.is_authenticated:
                usuario = request.user
            else:
                usuario, created = User.objects.get_or_create(
                    username="api_anonimo",
                    defaults={
                        "email": "api_anonimo@example.com",
                        "first_name": "API",
                        "last_name": "Anonimo"
                    }
                )
            
            # Ejecutar la compra
            total_pagado, orden_id = servicio.procesar(
                libro_id=datos['libro_id'],
                usuario=usuario,
                direccion=datos.get('direccion_envio', '')
            )
            
            if total_pagado:
                return Response({
                    "estado": "exito",
                    "mensaje": f"Orden #{orden_id} creada. Total: ${total_pagado}",
                    "orden_id": orden_id,
                    "total": total_pagado
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "error": "Error en el procesamiento del pago"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                "error": "Error interno del servidor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LibroListAPIView(APIView):
    """Endpoint para listar libros disponibles"""
    
    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)