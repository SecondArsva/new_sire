from django.db import models
from django.db.models.functions import Lower # case sensitive
from django.conf import settings # Para pillar el usuario a través del auth
from enum import Enum, auto

# Create your models here.

class Pais(models.Model):
    """Países disponibles en el sistema."""
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "core_pais"
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
        db_table = "core_ciudad"
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
        db_table = "core_operador"
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
        verbose_name="Operador",
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")

    class Meta:
        db_table = "core_reserva"
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
        db_table = "core_hotel"
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
        db_table = "core_guia"
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
        db_table = "core_tipo_momento"
        verbose_name = "Tipo (momento)"
        verbose_name_plural = "Tipos (momento)"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class TipoRemitente(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Pasajero
        - Operador
        - Minorista
        - Guía
        - Transferista
        - Receptivo
        - Departamento Interno
        - Otro
    """
    class Meta:
        db_table = "core_tipo_remitente"
        verbose_name = "Tipo (remitente)"
        verbose_name_plural = "Tipos (remitente)"
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
        db_table = "core_tipo_via_contacto"
        verbose_name = "Tipo (vías de contacto)"
        verbose_name_plural = "Tipos (vías de contacto)"
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
        db_table = "core_tipo_pagador"
        verbose_name = "Tipo (pagador)"
        verbose_name_plural = "Tipos (pagador)"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class TipoCausa(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - EMV
        - PAX
        - OPERATOR
        - DMC (Destination Management Company)
        - UNKNOWN
        - ¿¿¿ INFO ???
        - ¿¿¿ CONGRATS ???

    Adicionales por área:
    
    """

    class Meta:
        db_table = "core_tipo_causa"
        verbose_name = "Tipo (causa)"
        verbose_name_plural = "Tipos (causas)"
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
# - En lugar de usar models.TextChoices almacenado en un campo models.CharField
#   uso models.Model con registros según el tipo y lo recojo con un models.ForeignKey.

class IncidenciaCamposComunes(models.Model):
    """Campos comunes para cualquier incidencia (modelo abstracto)."""
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="%(class)ss",   # genérico para no chocar; no lo usarás en código
        verbose_name="Reserva",
        db_index=True,
    )
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
    causa = models.ForeignKey(
        TipoCausa,
        on_delete=models.PROTECT,
        verbose_name="Causa",
        db_index=True,
        null=True,
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
        help_text="Información adicional del caso (máx. 500)"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_creadas",
        verbose_name="Creado por",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        abstract = True # Autodescriptivo ¯\_(ツ)_/¯
        ordering = ["-created_at"]

class IncidenciaDemo(IncidenciaCamposComunes):
    """
    Incidencia Demo para ver como heredar los campos comunes.
    Tiene la misma estructura que las que se van a aplicar, pero sin campos extra.
    """
    class Meta:
        db_table = "core_incidencia_demo"
        verbose_name = "Incidencia (demo)"
        verbose_name_plural = "Incidencias (demo)"

class IncidenciaGuia(IncidenciaCamposComunes):
    # Sobreescritura de campos en los hijos para evitar
    # incompatibilidades con el related_name heredado.
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_guia",
        verbose_name="Reserva",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_guia_creadas",
        verbose_name="Creado por",
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
        db_table = "core_incidencia_guia"
        verbose_name = "Incidencia (guía)"
        verbose_name_plural = "Incidencias (guías)"
        ordering = ["-created_at"]

class Basico(models.Model):
    nombre = models.CharField(max_length=25, unique=True,)

    class Meta:
        db_table = "core_basico"
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
        db_table = "core_incidencia_transporte"
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
    habitacion = models.BooleanField(default=False)
    ubicacion = models.BooleanField(default=False)
    reservation = models.BooleanField(default=False)
    restaurante = models.BooleanField(default=False)
    otro = models.BooleanField(default=False)

    class Meta:
        db_table = "core_incidencia_hotel"
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

class TipoTransferistaIncidencia(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Pasajero ausente
        - Error del transferista
        - Encuentro no efectuado
        - Otros
    """
    class Meta:
        db_table = "core_tipo_transferista_incidencia"
        verbose_name = "Tipo (transferista - incidencia)"
        verbose_name_plural = "Tipos (transferista - incidencia)"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class TipoTransferistaPunto(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Aeropuerto / Hotel
        - Hotel / Aeropuerto
        - Terminal de buses / Hotel
        - Hotel / Terminal de buses
        - Hotel / Hotel
        - Estación de tren / Hotel
        - Hotel / Estación de tren
        - Puerto marítimo / Hotel
        - Hotel / Puerto marítimo
    """
    class Meta:
        db_table = "core_tipo_transferista_punto"
        verbose_name = "Tipo (transferista - punto)"
        verbose_name_plural = "Tipos (transferista - punto)"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class TipoTransferistaRazon(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Flight change
        - Flight delay
        - Lost Luggage
        - Airport Service (Passport control, Luggage pick-up)
        - PAX Error
        - TSF Error
        - Unknown                         (por defecto)
    """
    class Meta:
        db_table = "core_tipo_transferista_razon"
        verbose_name = "Tipo (transferista - razón)"
        verbose_name_plural = "Tipos (transferista - razón)"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

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

    # fecha???
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad",
        related_name="incidencias_transferista",
    )
    incidencia = models.ForeignKey(
        TipoTransferistaIncidencia,
        on_delete=models.PROTECT,
        verbose_name="Incidencia",
        db_index=True,
    )
    punto = models.ForeignKey(
        TipoTransferistaPunto,
        on_delete=models.PROTECT,
        verbose_name="Punto del viaje",
        db_index=True,
    )
    razon = models.ForeignKey(
        TipoTransferistaRazon,
        on_delete=models.PROTECT,
        verbose_name="Razón",
        db_index=True,
    )
    
    class Meta:
        db_table = "core_incidencia_transferista"
        verbose_name = "Incidencia (transferista)"
        verbose_name_plural = "Incidencias (transferista)"
        ordering = ["-created_at"]

class TipoOpcionalIncidencia(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - No realizado
        - Calidad del servicio
        - Impago
    """
    class Meta:
        db_table = "core_tipo_opcional_incidencia"
        verbose_name = "Tipo (opcional - incidencia)"
        verbose_name_plural = "Tipos (opcional - incidencia)"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class IncidenciaOpcional(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_opcional",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_opcional_creadas",
        verbose_name="Creado por"
    )

    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad",
        related_name="incidencias_opcionales",
    )
    #incidencia = models.CharField(
    #    max_length=3,
    #    choices=Incidencia.choices,
    #    verbose_name="Incidencia",
    #    db_index=True,
    #)
    incidencia = models.ForeignKey(
        TipoOpcionalIncidencia,
        on_delete=models.PROTECT,
        verbose_name="Incidencia",
        db_index=True,
    )

    class Meta:
        db_table = "core_incidencia_opcional"
        verbose_name = "Incidencia (opcional)"
        verbose_name_plural = "Incidencias (opcionales)"
        ordering = ["-created_at"]

class TipoOtroIncidencia(models.Model):
    nombre = models.CharField(max_length=50, unique=True,)
    """
    Opciones:
        - Causa médica
        - Robo / hurto
        - Objeto perdido / olvidado
        - Otro
    """
    class Meta:
        db_table = "core_tipo_otro_incidencia"
        verbose_name = "Tipo (otro - incidencia)"
        verbose_name_plural = "Tipos (otro - incidencia)"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class IncidenciaOtro(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_otro",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_otro_creadas",
        verbose_name="Creado por"
    )
    incidencia = models.ForeignKey(
        TipoOtroIncidencia,
        on_delete=models.PROTECT,
        verbose_name="Incidencia",
        db_index=True,
    )
    
    class Meta:
        db_table = "core_incidencia_otro"
        verbose_name = "Incidencia (otro)"
        verbose_name_plural = "Incidencias (otro)"
        ordering = ["-created_at"]

class IncidenciaTicket(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_ticket",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_ticket_creadas",
        verbose_name="Creado por"
    )
    origen = models.ForeignKey( # FROM
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de origen",
        related_name="incidencias_ticket_origen",
    )
    destino = models.ForeignKey( # TO
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de destino",
        related_name="incidencias_ticket_destino",
        null=True, blank=True,
    )
    
    class Meta:
        db_table = "core_incidencia_ticket"
        verbose_name = "Incidencia (ticket)"
        verbose_name_plural = "Incidencias (ticket)"
        ordering = ["-created_at"]

#class IncidenciaMytrip(IncidenciaCamposComunes): # Autotipado
#    # Sobreescritura del padre
#    reserva = models.ForeignKey(
#        Reserva,
#        on_delete=models.PROTECT,
#        related_name="incidencias_mytrip",
#        verbose_name="Reserva"
#    )
#    created_by = models.ForeignKey(
#        settings.AUTH_USER_MODEL,
#        on_delete=models.PROTECT,
#        related_name="incidencias_mytrip_creadas",
#        verbose_name="Creado por"
#    )
#    class Meta:
#        db_table = "core_incidencia_mytrip"
#        verbose_name = "Incidencia (mytrip)"
#        verbose_name_plural = "Incidencias (mytrip)"
#        ordering = ["-created_at"]
#
class IncidenciaItinerario(IncidenciaCamposComunes):
    '''
    Area para las actividades dentro del paquete turístico.
    Incluimos los tickets (ferry, boat...), vuelos incluidos (CAM),
    entradas de actividades (lo conocido como Entrada Museos)
    y un tipo de incidencia  "schedule". 4 checkbox.
    '''
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_itinerario",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_itinerario_creadas",
        verbose_name="Creado por",
    )
    # Incidencias
    schedule = models.BooleanField(default=False) # Horario (Fallo de EMV)
    ticket = models.BooleanField(default=False) # Entrada actividades. Entrada Museos, aunque sea el Bernabéu.
    trip = models.BooleanField(default=False) # Vuelos incluídos, tickets de ferris...
    
    origen = models.ForeignKey( # FROM
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de origen",
        related_name="incidencias_itinerario_origen",
    )
    destino = models.ForeignKey( # TO
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de destino",
        related_name="incidencias_itinerario_destino",
        null=True, blank=True,
    )

    class Meta:
        db_table = "core_incidencia_itinerario"
        verbose_name = "Incidencia (itinerario)"
        verbose_name_plural = "Incidencias (itinerarios)"
        ordering = ["-created_at"]

class IncidenciaMonumento(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_monumento",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_monumento_creadas",
        verbose_name="Creado por"
    )
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad",
        related_name="incidencias_monumento",
    )

    class Meta:
        db_table = "core_incidencia_monumento"
        verbose_name = "Incidencia (monumento)"
        verbose_name_plural = "Incidencias (monumentos)"
        ordering = ["-created_at"]

class IncidenciaVueloIncluido(IncidenciaCamposComunes):
    # Sobreescritura del padre
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="incidencias_vuelo_incluido",
        verbose_name="Reserva"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_vuelo_incluido_creadas",
        verbose_name="Creado por"
    )
    origen = models.ForeignKey( # FROM
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de origen",
        related_name="incidencias_vuelo_incluido_origen",
    )
    destino = models.ForeignKey( # TO
        Ciudad,
        on_delete=models.PROTECT,
        verbose_name="Ciudad de destino",
        related_name="incidencias_vuelo_incluido_destino",
        null=True, blank=True,
    )

    class Meta:
        db_table = "core_incidencia_vuelo_incluido"
        verbose_name = "Incidencia (vuelo incluido)"
        verbose_name_plural = "Incidencias (vuelos incluidos)"
        ordering = ["-created_at"]

# ʕ•ᴥ•ʔ
