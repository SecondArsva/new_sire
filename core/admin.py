from django.contrib import admin
# modelos
from .models import Pais, Ciudad
from .models import Operador, Reserva, Basico
from .models import Hotel, Guia
from .models import IncidenciaDemo, IncidenciaGuia, IncidenciaTransporte, IncidenciaHotel, IncidenciaTransferista, IncidenciaOpcionales

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
        'momento', 'remitente', 'via', 'pagador', 'importe', 'created_at',
        'comentario',
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
        'momento', 'remitente', 'via', 'pagador', 'importe', 'created_at',
        'comentario',
    )

@admin.register(IncidenciaTransporte)
class IncidenciaTransporteAdmin(admin.ModelAdmin):
    list_display=(
        'reserva',
        "basico", "origen", "destino", "conductor", "averia", "equipaje", "accidente", "otro",
        # Campos Comunes
        'momento', 'remitente', 'via', 'pagador', 'importe', 'created_at',
        'comentario',
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
        "room_key", "room_clean", "room_size", "room_bed_type", "room_facility",
        "room_amenity", "room_maintenance", "restaurant_personal", "restaurant_quantity",
        "restaurant_quality", "reserve_non_booking", "reserve_city_tax", "reserve_location",
        "other_personal", "other_lobby_size",
        "causa",
        # Campos Comunes
        'momento', 'remitente', 'via', 'pagador', 'importe', 'created_at',
        'comentario',
    )
    ordering = ["-created_at"]

@admin.register(IncidenciaTransferista)
class IncidenciaTransferistaAdmin(admin.ModelAdmin):
    list_display = (
        'reserva',
        "ciudad", "punto", "incidencia", "causa", "pax_avisado", "factura",
        # Campos Comunes
        'momento', 'remitente', 'via', 'pagador', 'importe', 'created_at',
        'comentario',
    )
    ordering = ["-created_at"]

@admin.register(IncidenciaOpcionales)
class IncidenciaOpcionalesAdmin(admin.ModelAdmin):
    list_display = (
        "reserva",
        "ciudad", "incidencia",
        # Campos Comunes
        'momento', 'remitente', 'via', 'pagador', 'importe', 'created_at',
        'comentario',
    )
    ordering = ["-created_at"]
