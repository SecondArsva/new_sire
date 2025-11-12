from django.db import models
from django.db.models.functions import Lower # case sensitive
from django.conf import settings # Para pillar el usuario a través del auth
from enum import Enum, auto

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
    apellido2 = models.CharField(max_length=50, verbose_name="Segundo Apellido",
                                 blank=True, default="")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Guía"
        verbose_name_plural = "Guías"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido1} {self.apellido2}".strip()

#   ╔═════════════╗
#   ║ Incidencias ║
#   ╚═════════════╝

class TipoMomento(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Antes del viaje
        - Durante el viaje
        - Después del viaje
    """
    class Meta:
        verbose_name = "Tipo de momento"
        verbose_name_plural = "Tipos de momento"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class TipoRemitente(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Cliente
        - Hotel
        - Guía
        - Agencia
        - Interno
        - Otro
    """
    class Meta:
        verbose_name = "Tipo de remitente"
        verbose_name_plural = "Tipos de remitente"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class TipoViaContacto(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Teléfono
        - Chat
        - Email
        - Otro
    """
    class Meta:
        verbose_name = "Tipo de vía de contacto"
        verbose_name_plural = "Tipos de vía de contacto"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class TipoPagador(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - EMV
        - PAX
        - Agencia
        - Nadie
    """
    class Meta:
        verbose_name = "Tipo de pagador"
        verbose_name_plural = "Tipos de pagador"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

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
    
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="%(class)ss",   # genérico para no chocar; no lo usarás en código
        verbose_name="Reserva",
        db_index=True,
    )

    #momento = models.CharField(
    #    max_length=5,
    #    choices=Momento.choices,
    #    verbose_name="Momento del viaje",
    #    db_index=True, # Revisa esto TODO
    #)
    #remitente = models.CharField(
    #    max_length=3,
    #    choices=Remitente.choices,
    #    verbose_name="Remitente",
    #    db_index=True, # Revisa esto TODO
    #)
    #via = models.CharField(
    #    max_length=3,
    #    choices=ViaContacto.choices,
    #    verbose_name="Vía de contacto",
    #    db_index=True, # Revisa esto TODO
    #)
    #pagador = models.CharField(
    #    max_length=3,
    #    choices=Pagador.choices,
    #    verbose_name="Pagador",
    #    db_index=True,
    #)
    momento = models.ForeignKey(
        TipoMomento,
        on_delete=models.PROTECT,
        verbose_name="Momento del viaje",
        db_index=True,
    )
    remitente = models.ForeignKey(
        TipoRemitente,
        on_delete=models.PROTECT,
        verbose_name="Remitente",
        db_index=True,
    )
    via = models.ForeignKey(
        TipoViaContacto,
        on_delete=models.PROTECT,
        verbose_name="Vía de contacto",
        db_index=True,
    )
    pagador = models.ForeignKey(
        TipoPagador,
        on_delete=models.PROTECT,
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
        related_name="%(class)s_creadas",
        verbose_name="Creado por",
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

class IncidenciaGuia(IncidenciaCamposComunes):
    # Sobreescritura de campos en los hijos para evitar
    # incompatibilidades con el related_name heredado.
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_guia",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_guia_creadas",
        verbose_name="Creado por"
    )
    # Campos propios de los guías.
    guia = models.ForeignKey(Guia, on_delete=models.PROTECT)
    # Tipos de incidencia
    personal = models.BooleanField(default=False)
    gestion = models.BooleanField(default=False)
    conocimiento = models.BooleanField(default=False)
    idioma = models.BooleanField(default=False)
    radio = models.BooleanField(default=False) # El Whisper
    otro = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Incidencia (guía)"
        verbose_name_plural = "Incidencias (guías)"
        ordering = ["-created_at"]

class Basico(models.Model):
    nombre = models.CharField(max_length=25, unique=True,)

    class Meta:
        verbose_name = "Sector básico"
        verbose_name_plural = "Sectores básicos"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre}"

class IncidenciaTransporte(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_transporte",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_transporte_creadas",
        verbose_name="Creado por"
    )
    # Campos de Transporte
    basico = models.ForeignKey(Basico, on_delete=models.PROTECT)
    origen = models.ForeignKey( # FROM
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de origen",
        related_name="incidencias_transporte_origen",
    )
    destino = models.ForeignKey( # TO
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de destino",
        related_name="incidencias_transporte_destino",
    )
    # Tipos de incidencia
    conductor = models.BooleanField(default=False)
    averia = models.BooleanField(default=False)
    equipaje = models.BooleanField(default=False)
    accidente = models.BooleanField(default=False)
    otro = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Incidencia (transporte)"
        verbose_name_plural = "Incidencias (transportes)"
        ordering = ["-created_at"]

class IncidenciaHotel(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_hotel",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_hotel_creadas",
        verbose_name="Creado por"
    )
    # Campos de Hotel
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    # Tipos de incidencia
    # ROOM
    room_key = models.BooleanField(default=False)
    room_clean = models.BooleanField(default=False)
    room_size = models.BooleanField(default=False)
    room_bed_type = models.BooleanField(default=False)
    room_facility = models.BooleanField(default=False)
    room_amenity = models.BooleanField(default=False)
    room_maintenance = models.BooleanField(default=False)
    # RESTAURANTE
    restaurant_personal = models.BooleanField(default=False)
    restaurant_quantity = models.BooleanField(default=False)
    restaurant_quality = models.BooleanField(default=False)
    # RESERVA
    reserve_non_booking = models.BooleanField(default=False)
    reserve_city_tax = models.BooleanField(default=False)
    reserve_location = models.BooleanField(default=False)
    # OTROS
    other_personal = models.BooleanField(default=False)
    other_lobby_size = models.BooleanField(default=False)

    causa = models.CharField(
        max_length=3,
        choices=[
            ("HTL", "Error Hotel"),
            ("EMV", "Error EMV"),
            ("UNK", "Desconocido"),
        ],
        verbose_name="Causa (Hotel)",
        db_index=True,
    )

    class Meta:
        verbose_name = "Incidencia (hotel)"
        verbose_name_plural = "Incidencias (hotel)"
        ordering = ["-created_at"]

    # Función rollo ft_is_tal() para futuros filtrados de cara a ver incidencias por subarea.
    def is_subincidence(self, subarea: str) -> bool:
        '''
        Recibe la flag de una subarea como str y analiza el registro para ver
        si hay alguna incidencia del subárea seleccionada.
        Flags: "ROOM", "REST", "RESE", "OTHE".
        '''
        if (subarea == "ROOM"):
            prefijo = "room_"
        elif (subarea == "REST"):
            prefijo = "restaurant_"
        elif (subarea == "RESE"):
            prefijo = "reserve_"
        elif (subarea == "OTHE"):
            prefijo = "other_"
        else:
            return False # subárea no relacionada
        
        for field in self._meta.get_field():
            if field.name.startswith(prefijo):
                if getattr(self, field.name):
                    return True
        return False

class IncidenciaTransferista(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_transferista",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_transferista_creadas",
        verbose_name="Creado por"
    )

    class Puto(models.TextChoices):
        APT_HTL = "APT/HTL", "Aeropuerto / Hotel"
        HTL_APT = "HTL/APT", "Hotel / Aeropuerto"

        TER_HTL = "TER/HTL", "Terminal de buses / Hotel"
        HTL_TER = "HTL/TER", "Hotel / Terminal de buses"

        HTL_HTL = "HTL/HTL", "Hotel / Hotel"

        STN_HTL = "STN/HTL", "Estación de tren / Hotel"
        HTL_STN = "HTL/STN", "Hotel / Estación de tren"

        PRT_HTL = "PRT/HTL", "Puerto marítimo / Hotel"
        HTL_PRT = "HTL/PRT", "Hotel / Puerto marítimo"

    class Incidencia(models.TextChoices):
        PAX_NO_SHOW = "PAX_NO_SHOW", "Pasajero ausente"
        TRF_ERROR = "TRF_ERROR", "Error del transferista"
        MISS_MEET = "MISS_MEET", "Encuentro no efectuado"
        OTHERS = "OTHERS", "Otros"

    class Causas(models.TextChoices):
        FLT_DELAY = "FLT_DELAY", "Vuelo retrasado"
        FLT_CHANGE = "FLT_CHANGE", "Cambio de vuelo"
        LOST_BAGGAGE = "LOST_BAGGAGE", "Equipaje perdido"
        APT_MGM = "APT_SVC_DELAY", "Administración aeropuerto"
        PAX_ERROR = "PAX_ERROR", "Error PAX"
        TRF_ERROR = "TRF_ERROR", "Error transferista"
        UNKNOWN = "UNKNOWN", "Desconocido"

    # fecha???
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad",
        related_name="incidencias_transferista",
    )
    punto = models.CharField(
        max_length=7,
        verbose_name="Punto del transfer",
        choices=Puto.choices,
        db_index=True, # Revisa esto TODO
    )
    incidencia = models.CharField(
        max_length=20,
        verbose_name="Incidencia",
        choices=Incidencia.choices,
        db_index=True,
    )
    causa = models.CharField(
        max_length=20,
        verbose_name="Causa",
        choices=Causas.choices,
        db_index=True,
    )
    class Meta:
        verbose_name = "Incidencia (transferista)"
        verbose_name_plural = "Incidencias (transferista)"
        ordering = ["-created_at"]

class IncidenciaOpcionales(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_opcionales",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_opcionales_creadas",
        verbose_name="Creado por"
    )

    class Incidencia(models.TextChoices):
        NO_REALIZADO = "NRL", "No realizado"
        CALIDAD = "QLT", "Calidad del servicio"
        IMPAGO = "IMP", "Impago"

    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad",
        related_name="incidencias_opcionales",
    )
    incidencia = models.CharField(
        max_length=3,
        choices=Incidencia.choices,
        verbose_name="Incidencia",
        db_index=True,
    )

    class Meta:
        verbose_name = "Incidencia (opcional)"
        verbose_name_plural = "Incidencias (opcionales)"
        ordering = ["-created_at"]

# Incidencias Autotipadas
# Modelos cuyas áreas representan directamente la incidencia a la que se
# refieren, sin tipos adicionales.
class IncidenciaMytrip(IncidenciaCamposComunes):
    class Meta:
        verbose_name = "Incidencia (mytrip)"
        verbose_name_plural = "Incidencias (mytrip)"
        ordering = ["-created_at"]

class IncidenciaItinerario(IncidenciaCamposComunes):
    class Meta:
        verbose_name = "Incidencia (itinerario)"
        verbose_name_plural = "Incidencias (itinerarios)"
        ordering = ["-created_at"]

class IncidenciaMonumento(IncidenciaCamposComunes):
    class Meta:
        verbose_name = "Incidencia (monumento)"
        verbose_name_plural = "Incidencias (monumentos)"
        ordering = ["-created_at"]

class IncidenciaVuelo(IncidenciaCamposComunes):
    class Meta:
        verbose_name = "Incidencia (vuelo)"
        verbose_name_plural = "Incidencias (vuelos)"
        ordering = ["-created_at"]
