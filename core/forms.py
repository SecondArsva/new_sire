# core/forms.py
from django import forms
# AUTH
from django.contrib.auth.forms import AuthenticationForm    # ╔══════╗
from django.contrib.auth.models import User                 # ║ AUTH ║
from django.contrib.auth import authenticate                # ╚══════╝

from .models import Operador, Hotel, Guia, Ciudad, Basico
from .models import IncidenciaCamposComunes
from .models import IncidenciaGuia, IncidenciaTransferista, IncidenciaOpcionales
from django.core.validators import RegexValidator

#   ╔══════╗
#   ║ AUTH ║
#   ╚══════╝
# Herencia de AuthenticationForm y personalización para poder entrar por email.
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No existe ninguna cuenta con ese correo.")

        self.user_cache = authenticate(
            self.request,
            username=user_obj.username,
            password=password
        )

        if self.user_cache is None:
            raise forms.ValidationError("Correo o contraseña incorrectos.")

        return self.cleaned_data
    
#   ╔══════════╗
#   ║ Reservas ║
#   ╚══════════╝
_localizador_validator = RegexValidator(
    regex=r"^[A-Z]{2}\d{6,8}$",
    message="Formato de localizador inválido: Introduce 2 letras en mayúscula y de 6 a 8 números"
)
class ReservaBuscarForm(forms.Form):
    localizador = forms.CharField(
        label="Buscar reserva",
        max_length=10,  # 2 letras + hasta 8 cifras
        validators=[_localizador_validator],
        widget=forms.TextInput(attrs={
            "placeholder": "Ej: AB123456",
            "autofocus": "autofocus"
        })
    )

    def clean_localizador(self):
        return self.cleaned_data["localizador"].strip().upper()

#*  No hay campo "localizador" en este form, ya que como se accede a la vista
#   de creación de reservas a través del buscador en caso de no existir la
#   reserva introducida, ya tenemos capturado el valor del localizador *#
class ReservaCrearForm(forms.Form):
    operador = forms.ModelChoiceField(
        label="Operador",
        required=True,
        queryset= Operador.objects.none(), # Precisa de un queryset
    )
    fecha_inicio = forms.DateField(
        label="Fecha de inicio",
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",          # activa el selector nativo
                "class": "form-control", # opcional, para Bootstrap o estilo propio
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(ReservaCrearForm, self).__init__(*args, **kwargs)
        self.fields["operador"].queryset = Operador.objects.filter(is_active=True).order_by("nombre")

#   ╔═════════════╗
#   ║ Incidencias ║
#   ╚═════════════╝
class IncidenciaCamposComunesForm(forms.Form):
    """Formulario de captura de datos para los campos comunes que ha de introducir el usuario"""
    momento = forms.ChoiceField(
        label="Momento del viaje",
        choices=[("", "---------")] + list(IncidenciaCamposComunes.Momento.choices),
        required=True,
    )
    remitente = forms.ChoiceField(
        label="Remitente",
        choices=[("", "---------")] + list(IncidenciaCamposComunes.Remitente.choices),
        required=True,
    )
    via = forms.ChoiceField(
        label="Vía de contacto",
        choices=[("", "---------")] + list(IncidenciaCamposComunes.ViaContacto.choices),
        required=True,
    )
    pagador = forms.ChoiceField(
        label="Pagador",
        choices=[("", "---------")] + list(IncidenciaCamposComunes.Pagador.choices),
        required=True,
    )
    importe = forms.DecimalField(
        label="Importe (€)",
        min_value=0,
        max_digits=10,
        decimal_places=2,
        initial=0,
        help_text="Importe económico si aplica"
    )
    comentario = forms.CharField(
        label="Comentario",
        widget=forms.Textarea(attrs={"rows":7}),
        required=True,
        max_length=500,
    )

class IncidenciaDemoForm(IncidenciaCamposComunesForm):
    """Demostración de la herencia, sin campos añadidos.""" # Celia Juver Cruz'nt lol
    pass

class IncidenciaGuiaForm(IncidenciaCamposComunesForm):
    """Formulario para las incidencias relacionadas a los guías."""
    guia = forms.ModelChoiceField(
        queryset=Guia.objects.none(),
        label="Guía",
        required=True,
        empty_label="Selecciona un guía",)
    personal = forms.BooleanField(label="PERSONAL", required=False, initial=False)
    gestion = forms.BooleanField(label="GESTIÓN", required=False, initial=False)
    conocimiento = forms.BooleanField(label="CONOCIMIENTO", required=False, initial=False)
    idioma = forms.BooleanField(label="IDIOMA", required=False, initial=False)
    radio = forms.BooleanField(label="RADIO (Whisper)", required=False, initial=False)
    otro = forms.BooleanField(label="OTRO", required=False, initial=False)

    # Personalización del orden en que se renderizan los campos. Primero los de guía, luego los comunes.
    field_order = [
        "guia", "personal", "gestion", "conocimiento", "idioma", "radio", "otro",
        # Campos Comunes
        "momento", "remitente", "via", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["guia"].queryset = Guia.objects.filter(is_active=True).order_by("nombre")
        self.order_fields(self.field_order)  # asegura el orden

class IncidenciaTransporteForm(IncidenciaCamposComunesForm):
    basico = forms.ModelChoiceField(
        queryset=Basico.objects.none(),
        label="Básico",
        required=True,
        empty_label="Selecciona el sector básico",)
    origen = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Origen",
        required=True,
        empty_label="Selecciona una ciudad",)
    destino = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Destino",
        required=True,
        empty_label="Selecciona una ciudad",)

    conductor = forms.BooleanField(label="CONDUCTOR", required=False, initial=False)
    averia = forms.BooleanField(label="AVERÍA", required=False, initial=False)
    equipaje = forms.BooleanField(label="EQUIPAJE", required=False, initial=False)
    accidente = forms.BooleanField(label="ACCIDENTE", required=False, initial=False)
    otro = forms.BooleanField(label="OTRO", required=False, initial=False)

    field_order = [
        "basico", "origen", "destino", "conductor", "averia", "equipaje", "accidente", "otro",
        # Campos Comunes
        "momento", "remitente", "via", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["basico"].queryset = Basico.objects.all().order_by("nombre")
        self.fields["origen"].queryset = Ciudad.objects.all().order_by("nombre")
        self.fields["destino"].queryset = Ciudad.objects.all().order_by("nombre")

class IncidenciasHotelForm(IncidenciaCamposComunesForm):
    hotel = forms.ModelChoiceField(
        queryset=Basico.objects.none(),
        label="Hotel",
        required=True,
        empty_label="Nombre del hotel",
    )
    # Tipos de incidencia
    # ROOM
    room_key = forms.BooleanField(label="KEY", required=False, initial=False)
    room_clean = forms.BooleanField(label="CLEAN", required=False, initial=False)
    room_size = forms.BooleanField(label="SIZE", required=False, initial=False)
    room_bed_type = forms.BooleanField(label="BED TYPE", required=False, initial=False)
    room_facility = forms.BooleanField(label="FACILITY", required=False, initial=False)
    room_amenity = forms.BooleanField(label="AMENITY", required=False, initial=False)
    room_maintenance = forms.BooleanField(label="MAINTENANCE", required=False, initial=False)
    # RESTAURANTE
    restaurant_personal = forms.BooleanField(label="PARSONAL", required=False, initial=False)
    restaurant_quantity = forms.BooleanField(label="QUANTITY", required=False, initial=False)
    restaurant_quality = forms.BooleanField(label="QUALITY", required=False, initial=False)
    # RESERVA
    reserve_non_booking = forms.BooleanField(label="NON BOOKING", required=False, initial=False)
    reserve_city_tax = forms.BooleanField(label="CITY TAX", required=False, initial=False)
    reserve_location = forms.BooleanField(label="LOCATION", required=False, initial=False)
    # OTROS
    other_personal = forms.BooleanField(label="PERSONAL", required=False, initial=False)
    other_lobby_size = forms.BooleanField(label="LOBBY SIZE", required=False, initial=False)

    causa = forms.ChoiceField(
        label="Causa",
        choices=[("", "---------")] + [("HTL", "Error Hotel"), ("EMV", "Error EMV"), ("UNK", "Desconocido"),],
        required=True,
    )

    field_order = [
        "hotel",
        "room_key", "room_clean", "room_size", "room_bed_type", "room_facility",
        "room_amenity", "room_maintenance", "restaurant_personal", "restaurant_quantity",
        "restaurant_quality", "reserve_non_booking", "reserve_city_tax", "reserve_location",
        "other_personal", "other_lobby_size",
        "causa",
        # Campos Comunes
        "momento", "remitente", "via", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hotel"].queryset = Hotel.objects.all().order_by("nombre")

class IncidenciaTransferistaForm(IncidenciaCamposComunesForm):
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Ciudad",
        required=True,
        empty_label="Selecciona una ciudad",)
    punto = forms.ChoiceField(
        label="Punto",
        choices=[("", "---------")] + list(IncidenciaTransferista.Puto.choices),
        required=True,
    )
    incidencia = forms.ChoiceField(
        label="Incidencia",
        choices=[("", "---------")] + list(IncidenciaTransferista.Incidencia.choices),
        required=True,
    )
    causa = forms.ChoiceField(
        label = "Causa",
        choices=[("", "---------")] + list(IncidenciaTransferista.Causas.choices),
        required=True,
    )
    pax_avisado = forms.BooleanField(label="Pasajero Avisado", required=False, initial=False)
    factura = forms.BooleanField(label="Factura", required=False, initial=False)

    field_order = [
        "ciudad", "punto", "incidencia", "causa", "pax_avisado", "factura",
        # Campos Comunes
        "momento", "remitente", "via", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ciudad"].queryset = Ciudad.objects.all().order_by("nombre")

class IncidenciaOpcionalesForm(IncidenciaCamposComunesForm):
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Ciudad",
        required=True,
        empty_label="Selecciona una ciudad",)
    incidencia = forms.ChoiceField(
        label="Incidencia",
        choices=[("", "---------")] + list(IncidenciaOpcionales.Incidencia.choices),
        required=True,
    )

    field_order = [
        "ciudad", "incidencia",
        # Campos Comunes
        "momento", "remitente", "via", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ciudad"].queryset = Ciudad.objects.all().order_by("nombre")
