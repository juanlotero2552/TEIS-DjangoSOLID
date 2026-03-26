from .models import Libro, Inventario
from .domain.calculadores import CalculadorImpuestos
from .domain.builders import OrdenBuilder
from django.contrib.auth.models import User

class CompraRapidaService:
    """
    Servicio que maneja la lógica de negocio de compras rápidas
    usando Factory Method y Builder
    """
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()
    
    def procesar(self, libro_id, usuario, direccion=None):
        """
        Procesa la compra de un libro
        Args:
            libro_id: ID del libro a comprar
            usuario: Objeto User de Django (no el ID)
            direccion: Dirección de envío (opcional)
        Returns:
            tuple: (total_pagado, orden_id) o (None, None) si falla
        """
        # Obtener el libro y su inventario
        libro = Libro.objects.get(id=libro_id)
        inventario = Inventario.objects.get(libro=libro)
        
        # Validar que hay stock
        if inventario.cantidad <= 0:
            raise ValueError("❌ No hay existencias disponibles.")
        
        # Calcular total con IVA
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        
        # Procesar el pago
        if self.procesador_pago.pagar(total):
            # Actualizar inventario
            inventario.cantidad -= 1
            inventario.save()
            
            # Construir orden usando Builder Pattern
            orden = (self.builder
                    .con_usuario(usuario)  # usuario es objeto User
                    .con_productos([libro])
                    .para_envio(direccion or "Retiro en tienda")
                    .build())
            
            return total, orden.id
        
        return None, None


# ✅ ALIAS PARA COMPATIBILIDAD CON CÓDIGO EXISTENTE
# Esto permite que otras partes del código que importan "CompraService" sigan funcionando
CompraService = CompraRapidaService
