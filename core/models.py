from django.db import models
from django.db.models.functions import Lower # case sensitive
from django.conf import settings # Para pillar el usuario a través del auth

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

#   ╔═════════════╗
#   ║ Incidencias ║
#   ╚═════════════╝
# - reserva, un FK al registro de la reserva a la que corresponde.
# - momento, CharField momento del viaje en eque se dio (pre, durante o post viaje)
# - remitente, charfield (¿Quién llama?)
# - via, charfield (via usada por el remitente para contactar)
# - pagador, charfield (nombre original "extra_payment", ¿quién paga el pato? Empres, cliente, agencia o nadie)
# - importe, no sé muy bien como definirlo. Es el importe a pagar de la devolución o compensación. El tema es que un compañero me ha dicho que use dos enteros, € y cents. Pero luego como lo mergeo? Lo pillo en el form con dos campos y luego formateo el importe correctamente?
# - comentario, charfield max=1000, info del caso
# - usuario, charfield pilla el nombre del usuario que rellenó el caso
# - timestamp datetime automático
class IncidenciaCamposComunes(models.Model):
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias",
        verbose_name="Reserva",
        db_index=True, # Revisa esto TODO
    )
    
    

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_creadas",
        verbose_name="Creado por"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")
    
    class Meta:
        abstract = True # Autodescriptivo ¯\_(ツ)_/¯
        ordering = ["-created_at"]

class IncidenciasHotel(IncidenciasCamposComunes):
    hotel = models.ForeignKey()
