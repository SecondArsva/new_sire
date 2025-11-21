from django.contrib import admin
# modelos
from .models import Pais, Ciudad
from .models import Operador, Reserva, Basico, Opcional
from .models import Hotel, Guia
from .models import IncidenciaDemo, IncidenciaGuia, IncidenciaTransporte
from .models import IncidenciaHotel, IncidenciaTransferista, IncidenciaOpcional
from .models import IncidenciaOtro
from .models import TipoMomento, TipoRemitente, TipoViaContacto, TipoPagador, TipoCausa, TipoOtroIncidencia
from .models import TipoTransferistaIncidencia, TipoTransferistaPunto
from .models import IncidenciaGeneral, IncidenciaItinerario

# Register your models here.

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'is_active')

@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'is_active')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('localizador', 'operador', 'fecha_inicio',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'is_active')
    ordering = ["nombre"]

@admin.register(IncidenciaDemo)
class IncidenciaDemo(admin.ModelAdmin):
    list_display = (
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )
    ordering = ['-created_at']

@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido1', 'apellido2', 'is_active')
    ordering = ['nombre']

@admin.register(IncidenciaGuia)
class IncidenciaGuiaAdmin(admin.ModelAdmin):
    list_display=(
        'reserva',
        "guia", "personal", "gestion", "conocimiento", "idioma", "radio", "otro",
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )

@admin.register(IncidenciaTransporte)
class IncidenciaTransporteAdmin(admin.ModelAdmin):
    list_display=(
        'reserva',
        #"basico", "origen", "destino",
        "conductor", "averia", "equipaje", "accidente", "otro",
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )

@admin.register(Basico)
class BasicoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ["nombre"]

@admin.register(IncidenciaHotel)
class IncidenciaHotelAdmin(admin.ModelAdmin):
    list_display=(
        'reserva',
        "hotel",
        "habitacion", "ubicacion", "reservation", "restaurante", "otro",
        "causa",
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )
    ordering = ["-created_at"]

@admin.register(IncidenciaTransferista)
class IncidenciaTransferistaAdmin(admin.ModelAdmin):
    list_display = (
        'reserva',
        "ciudad", "punto", "incidencia", "causa",
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )
    ordering = ["-created_at"]

@admin.register(IncidenciaOpcional)
class IncidenciaOpcionalAdmin(admin.ModelAdmin):
    list_display = (
        "reserva",
        "opcional", 
        "inc_no_realizado", "inc_devolucion", "inc_pack", "inc_otros", 
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )
    ordering = ["-created_at"]

@admin.register(TipoMomento)
class TipoMomentoAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

@admin.register(TipoRemitente)
class TipoRemitenteAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

@admin.register(TipoViaContacto)
class TipoViaContactoAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

@admin.register(TipoPagador)
class TipoPagadorAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

@admin.register(TipoCausa)
class TipoCausaAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

@admin.register(TipoTransferistaIncidencia)
class TipoTransferistaIncidenciaAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

@admin.register(TipoTransferistaPunto)
class TipoTransferistaPuntoAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

#@admin.register(TipoTransferistaRazon)
#class TipoTransferistaRazonAdmin(admin.ModelAdmin):
#    list_display = ("pk", "nombre",)
#    ordering = ["pk", "nombre"]

@admin.register(Opcional)
class OpcionalAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

#@admin.register(TipoOpcionalIncidencia)
#class OpcionalIncidenciaAdmin(admin.ModelAdmin):
#    list_display=(
#        'reserva',
#        '', '', '', '', '',
#        # Campos Comunes
#        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
#        'comentario', "is_active",
#    )

@admin.register(TipoOtroIncidencia)
class TipoOtroIncidenciaAdmin(admin.ModelAdmin):
    list_display = ("pk", "nombre",)
    ordering = ["pk", "nombre"]

@admin.register(IncidenciaOtro)
class IncidenciaOtroAdmin(admin.ModelAdmin):
    list_display=(
        'reserva',
        'incidencia',
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )

@admin.register(IncidenciaGeneral)
class IncidenciaGeneralAdmin(admin.ModelAdmin):
    list_display=(
        'reserva',
        'inc_personal', 'inc_seguro', 'inc_otros',
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )

@admin.register(IncidenciaItinerario)
class IncidenciaItinerarioAdmin(admin.ModelAdmin):
    list_display=(
        'reserva',
        'ciudad',
        'inc_itinerario', 'inc_entradas', 'inc_billetes', 'inc_guia_local', 'inc_comidas', 
        # Campos Comunes
        'momento', 'remitente', 'via', 'causa','pagador', 'importe', 'created_at', 'created_by',
        'comentario', "is_active",
    )
