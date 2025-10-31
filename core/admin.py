from django.contrib import admin
# modelos
from .models import Pais, Ciudad
from .models import Operador, Reserva
from .models import Hotel, Guia
from .models import IncidenciaDemo

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
    list_display = ('reserva', 'momento', 'remitente', 'via', 'pagador', 'importe', 'created_at',)
    ordering = ['-created_at']

@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido1', 'apellido2', 'is_active')
