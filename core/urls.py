from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("reserva/<str:localizador>/", views.reserva_ver, name="reserva_ver"),
    path("reserva/nueva/<str:localizador>/", views.reserva_crear, name="reserva_crear"),
    #path("reserva/with/", views.)
]
