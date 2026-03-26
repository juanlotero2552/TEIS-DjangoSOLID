from decimal import Decimal

class CalculadorImpuestos:
    """Calcula impuestos para las transacciones usando Decimal"""
    
    IVA = Decimal('0.19')  # 19% de IVA como Decimal
    
    @classmethod
    def obtener_total_con_iva(cls, precio):
        """
        Calcula el precio total incluyendo IVA
        Args:
            precio: Decimal o float (se convertirá a Decimal)
        Returns:
            Decimal: precio con IVA incluido
        """
        # Convertir a Decimal si es necesario
        if not isinstance(precio, Decimal):
            precio = Decimal(str(precio))
        
        return precio * (Decimal('1') + cls.IVA)