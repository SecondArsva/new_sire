from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # Autenticación
#FORMS
from .forms import ReservaBuscarForm, ReservaCrearForm, IncidenciaAreaForm
#MODELS
from .models import Reserva
from django.contrib import messages

# Create your views here.

# Hola mundo de prueba
@login_required
def home(request):
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
    return render(request, "core/reserva_ver.html", {"reserva": reserva})

@login_required
def reserva_crear(request, localizador: str):
    # Aquí podrías inicializar tu formulario de creación con el localizador
    # form = ReservaForm(initial={"localizador": localizador})
    # return render(request, "reserva_crear.html", {"form": form})

    # Diseño
    # Por si las moscas, si un usuario lograse acabar aquí al introducir un
    # localizador ya existente en la DB, se le redirige al reserva_ver, de ese
    # localizador.
    # Como no va a existir, se pilla y se crea si el ReservaCrearForm está bien.
    # Cuando se crea y se registra se manda a la selección de tipo de incidencia.

    #return render(request, "core/reserva_crear.html", {"localizador": localizador})
    
    # 1) Si ya existe, redirige al visor de esa reserva
    existente = Reserva.objects.filter(localizador=localizador).first()
    if existente:
        messages.info(request, f"La reserva {localizador} ya existe. Te llevo a su visor.")
        return redirect("core:reserva_ver", localizador=localizador)

    # 2) Si NO existe, flujo normal de creación
    if request.method == "POST":
        form = ReservaCrearForm(request.POST)
        if form.is_valid():
            reserva = Reserva.objects.create(
                localizador=localizador, # viene en URL
                operador=form.cleaned_data["operador"],
                fecha_inicio=form.cleaned_data["fecha_inicio"],
            )
            messages.success(request, f"Reserva {localizador} creada correctamente.")
            # 3) Redirige a la selección de tipo de incidencia (ajusta el nombre de la URL)
            return redirect("core:reserva_ver", localizador=reserva.localizador)
    else:
        form = ReservaCrearForm()

    return render(
        request,
        "core/reserva_crear.html",
        {"form": form, "localizador": localizador},
    )

#@login_required
#def incidencia_area(request): # TODO
#    if request.method == "POST":
#        form = IncidenciaAreaForm(request.POST)
#        if form.is_valid():
#            area = form.cleaned_data["area"]
#            request.session["reporte_area"] = area  # guarda string ("HOTEL", etc.)
#            request.session.modified = True
#            #return redirect("core:filler_spa")
#    else:
#        form = IncidenciaAreaForm()
#
#    return render(request, "core/incidencia_area.html", {"form": form})
