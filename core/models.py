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

class Guia(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido1 = models.CharField(max_length=50, verbose_name="Primer Apellido")
    apellido2 = models.CharField(max_length=50, verbose_name="Segundo Apellido")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Guía"
        verbose_name_plural = "Guías"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido1} {self.apellido2}" if self.apellido2 else f"{self.nombre} {self.apellido1}"

#   ╔═════════════╗
#   ║ Incidencias ║
#   ╚═════════════╝

#   ╔═════════════╗
#   ║ TextChoices ║
#   ╚═════════════╝
class Momento(models.TextChoices):
    PRE = "PRE", "Antes del viaje"
    DUR = "DUR", "Durante el viaje"
    POST = "POST", "Después del viaje"

class Remitente(models.TextChoices):
    CLIENTE = "CLI", "Cliente"
    HOTEL = "HOT", "Hotel"
    GUIA = "GUI", "Guía"
    AGENCIA = "AGE", "Agencia"
    INTERNO = "INT", "Interno"
    OTRO = "OTR", "Otro"

class ViaContacto(models.TextChoices):
    TELEFONO = "TEL", "Teléfono"
    EMAIL = "EML", "Email"
    WHATSAPP = "WHA", "WhatsApp"
    OTRO = "OTR", "Otros"
    # HappyFaces
    # MyTryp

class Pagador(models.TextChoices):
    EMV = "EMV", "EMV"
    CLIENTE = "CLI", "Cliente"
    AGENCIA = "AGE", "Agencia"
    NONE = "NON", "Nadie"

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
    """Campos comunes para cualquier incidencia (modelo abstracto)."""
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias",
        verbose_name="Reserva",
        db_index=True, # Revisa esto TODO
    )

    momento = models.CharField(
        max_length=5,
        choices=Momento.choices,
        verbose_name="Momento del viaje",
        db_index=True, # Revisa esto TODO
    )
    remitente = models.CharField(
        max_length=3,
        choices=Remitente.choices,
        verbose_name="Remitente",
        db_index=True, # Revisa esto TODO
    )
    via = models.CharField(
        max_length=3,
        choices=ViaContacto.choices,
        verbose_name="Vía de contacto",
        db_index=True, # Revisa esto TODO
    )
    pagador = models.CharField(
        max_length=3,
        choices=Pagador.choices,
        verbose_name="Pagador",
        db_index=True,
    )
    importe = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Importe (€)"
    )

    comentario = models.TextField(
        max_length=500,
        verbose_name="Comentario",
        help_text="Información adicional del caso (máx. 1000)"
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

class IncidenciaDemo(IncidenciaCamposComunes):
    """
    Incidencia Demo para ver como heredar los campos comunes.
    Tiene la misma estructura que las que se van a aplicar, pero sin campos extra.
    """
    class Meta:
        verbose_name = "Incidencia (demo)"
        verbose_name_plural = "Incidencias (demo)"