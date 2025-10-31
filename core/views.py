import re
from django.shortcuts import render, redirect, get_object_or_404
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required # Autenticación
from django.contrib import messages
#FORMS
from .forms import ReservaBuscarForm, ReservaCrearForm
from .forms import IncidenciaDemoForm
#MODELS
from .models import Reserva
from .models import IncidenciaDemo

# Create your views here.

# Como meter datos mediante la URL es un mierdón, voy a usar un dict session_state
# como de costumbre para la correcta recolección y paso de datos.
# Helpers del session_state ---
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

#   ╔═════════════╗
#   ║ Incidencias ║
#   ╚═════════════╝
@login_required
def incidencia_area(request): # Botones de selección en template.
    return render(request, "core/incidencia_area.html")

FORM_STATE_KEY = "incidencia_demo"
@login_required
def incidencia_demo(request: HttpRequest) -> HttpResponse:
    # 0) Pillamos el locata a través del session_state
    state: dict = _get_state(request.session)
    localizador = state.get("localizador")

    # 1) Control de errores.
    if not localizador:
        print("Error: No hay locata: Intento de acceso sin pasar por el buscador de reservas")
        return redirect("core:home")
    
    # 2) Búsqueda del registro de la reseva mediante el locata y si falla, error.
    # Equivale a:
    #       try:
    #           reserva = Reserva.objects.get(localizador=localizador)
    #       except Reserva.DoesNotExist:
    #           raise Http404("Reserva no encontrada")
    reserva = get_object_or_404(Reserva, localizador=localizador)

    if request.method == "POST":
        form = IncidenciaDemoForm(request.POST)
        if form.is_valid():
            # (Opcional) guarda una copia en sesión por si luego quieres reusar
            _set_state(request.session, FORM_STATE_KEY, form.cleaned_data)

            IncidenciaDemo.objects.create(
                reserva=reserva,
                created_by=request.user,
                **form.cleaned_data,
                # Como los campos del form y del model coinciden se pasan todos los
                # valores a través del desempaquetado de **kwargs en Python.
            )
            print("Incidencia demo creada.")
            messages.success(request, "Incidencia demo creada.")
            # si quieres limpiar los datos del form en sesión tras crear:
            _set_state(request.session, SESSION_KEY, {})
            return redirect("core:incidencia_demo")
    else:
        # prefill desde sesión (opcional)
        initial = state.get(FORM_STATE_KEY, {})
        form = IncidenciaDemoForm(initial=initial)
    context = {
        "reserva": reserva,
        "form": form,
    }
    return render(request, "core/incidencia_demo.html", context)

@login_required
def incidencia_guia(request):
    pass
