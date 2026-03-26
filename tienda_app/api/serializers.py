from rest_framework import serializers
from tienda_app.models import Libro, Orden

class LibroSerializer(serializers.ModelSerializer):
    """Serializer para mostrar información de libros"""
    stock_actual = serializers.IntegerField(source='inventario.cantidad', read_only=True)
    
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio', 'stock_actual']


class OrdenInputSerializer(serializers.Serializer):
    """
    Serializer para VALIDAR la entrada de datos.
    Actúa como un DTO (Data Transfer Object).
    """
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200, required=False, allow_blank=True)
    
    def validate_libro_id(self, value):
        """Validación personalizada: verificar que el libro existe"""
        from tienda_app.models import Libro
        if not Libro.objects.filter(id=value).exists():
            raise serializers.ValidationError("El libro no existe")
        return value
