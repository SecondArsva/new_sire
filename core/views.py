import re
from django.shortcuts import render, redirect, get_object_or_404
from typing import Any
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # Autenticación
#FORMS
from .forms import ReservaBuscarForm, ReservaCrearForm, IncidenciaAreaForm
#MODELS
from .models import Reserva

# Create your views here.

# Como meter datos mediante la URL es un mierdón, voy a usar un dict session_state
# como de costumbre para la correcta recolección y paso de datos.
SESSION_KEY:str="dict_state"

def _get_state(session) -> dict:
    return session.get(SESSION_KEY, {})

def _set_state(session, key: str, value):
    state = _get_state(session)
    state[key] = value
    session[SESSION_KEY] = state
    session.modified = True

def _clear_state(session):
    session.pop(SESSION_KEY, None)
    session.modified = True

@login_required
def home(request): # LoDelNombre... ¯\_(ツ)_/¯
    # Limpiamos el ession_state en caso de existir
    if _get_state(request.session):
        _clear_state(request.session)
        print("HOME: Session_state existente detectado: Contenido Eliminado")

    # Inicio del SIRE. Búsqueda por localizador.
    if request.method == "POST":
        form = ReservaBuscarForm(request.POST)
        if form.is_valid():
            loc = form.cleaned_data["localizador"]
            print(f"Locata pillado: {loc}")
            # Si existe, vamos al visor:
            if Reserva.objects.filter(localizador=loc).exists():
                return redirect("core:reserva_ver", localizador=loc)
            else: # Si no existe, creamos
                return redirect("core:reserva_crear", localizador=loc)
    else:
        form = ReservaBuscarForm()
    # Si GET o form inválido, renderiza el home con el form
    return render(request, "core/home.html", {"form_buscar": form})

@login_required
def reserva_ver(request, localizador: str):
    reserva = get_object_or_404(Reserva, localizador=localizador)
    print(f"(reserva_ver_view) reserva.id: {reserva.id}")
    print(f"(reserva_ver_view) reserva.id: {reserva.localizador}")
    print(f"(reserva_ver_view) reserva.id: {reserva.operador}")
    print(f"(reserva_ver_view) reserva.id: {reserva.fecha_inicio}")

    state: dict = _get_state(request.session)
    _set_state(request.session, "localizador", reserva.localizador)

    return render(request, "core/reserva_ver.html", {"reserva": reserva})

@login_required
def reserva_crear(request, localizador: str):
    # 0) Para evitar que el usuario acceda a la creación de una nueva reserva
    # mediante "http://127.0.0.1:1313/reserva/nueva/<str:localizador>/" en el
    # browser y genere reservas con localizadores fuera del formato permitido,
    # comprobamos el valor del str de la URL. Si no es correcto volvemos al HOME.
    if not re.match(r"^[A-Z]{2}\d{6,8}$", localizador):
        return redirect("core:home")

    # 1) Si ya existe, redirige al visor de esa reserva. Control por si el usuario
    # regresase desde el browser tras añadir una nueva incidencia.
    existente = Reserva.objects.filter(localizador=localizador).first()
    if existente:
        return redirect("core:reserva_ver", localizador=localizador)

    # 2) Si no existe, flujo normal de creación
    if request.method == "POST":
        form = ReservaCrearForm(request.POST)
        if form.is_valid():
            reserva = Reserva.objects.create(
                localizador=localizador, # viene en URL
                operador=form.cleaned_data["operador"],
                fecha_inicio=form.cleaned_data["fecha_inicio"],
            )
            # 3) Redirige a la selección de tipo de incidencia (ajusta el nombre de la URL)
            return redirect("core:reserva_ver", localizador=reserva.localizador)
    else:
        form = ReservaCrearForm()

    return render(
        request, "core/reserva_crear.html",
        {"form": form, "localizador": localizador},
    )

@login_required
def incidencia_nueva_area(request): # Botones de selección en template.
    return render(request, "core/incidencia_nueva_area.html")

@login_required
def incidencia_nueva_hotel(request):
    # estado
    # POST formulario
    # if oki, regist
    # Not re-render
    return render(request, "core/incidencia_nueva_hotel.html")
