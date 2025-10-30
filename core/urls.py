from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("reserva/<str:localizador>/", views.reserva_ver, name="reserva_ver"),
    path("reserva/nueva/<str:localizador>/", views.reserva_crear, name="reserva_crear"),
    path("incidencia/nueva/area", views.incidencia_nueva_area, name="incidencia_nueva_area"),
    path("incidencia/nueva/hotel", views.incidencia_nueva_hotel, name="incidencia_nueva_hotel"),
]
