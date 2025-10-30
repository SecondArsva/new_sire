from django.contrib import admin
# modelos
from .models import Pais, Ciudad, Operador, Reserva
from .models import Hotel

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
    list_display = ('nombre', 'ciudad')
    