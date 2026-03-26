from decimal import Decimal
from ..models import Orden

class OrdenBuilder:
   
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._usuario = None
        self._items = []
        self._direccion = ""
        return self
    
    def con_usuario(self, usuario):
        self._usuario = usuario
        return self
    
    def con_productos(self, productos):
        self._items = productos
        return self
    
    def para_envio(self, direccion):
        self._direccion = direccion
        return self
    
    def build(self) -> Orden:
        if not self._usuario or not self._items:
            raise ValueError("Datos insuficientes para crear la orden.")
        
        subtotal = Decimal('0')
        for item in self._items:
            subtotal += item.precio 
        
        iva = Decimal('0.19')
        total_con_iva = subtotal * (Decimal('1') + iva)

        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=self._items[0] if self._items else None,
            total=total_con_iva,  
            direccion_envio=self._direccion
        )
        
        self.reset()
        return orden