from django.db import models
from django.db.models.functions import Lower # case sensitive

# Create your models here.

class Pais(models.Model):
    """Países disponibles en el sistema."""
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    """Ciudades disponibles en el sistema"""
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,
        related_name="ciudades",
        verbose_name="País",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ["nombre"]
        unique_together = ("nombre", "pais")

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"

class Operador(models.Model):
    """Operadores disponibles en el sistema"""
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,
        related_name="operadores",
        verbose_name="País",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"
        ordering = ["nombre"]
        unique_together=("nombre", "pais")

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"

class Reserva(models.Model):
    """Reservas disponibles en el sistema"""
    localizador = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Localizador",)
    operador = models.ForeignKey(
        Operador,
        on_delete=models.PROTECT,
        related_name="reservas",
        verbose_name="Operador"
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.localizador}"

class Hotel(models.Model):
    """Hoteles disponibles en el sistema"""
    nombre = models.CharField(
        max_length=100,
        verbose_name="Hotel",
    )
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        related_name="hoteles",
        verbose_name="Ciudad",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hoteles"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "ciudad"], name="unique_hotel_per_city"
            ),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.ciudad.nombre})"
    
class IncidenciaHotel(models.Model):
    """Incidencias de hoteles disponibles en el sistema"""
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    incidencia = models.CharField()
