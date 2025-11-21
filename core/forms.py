# core/forms.py
from django import forms
# AUTH
from django.contrib.auth.forms import AuthenticationForm    # ╔══════╗
from django.contrib.auth.models import User                 # ║ AUTH ║
from django.contrib.auth import authenticate                # ╚══════╝

from .models import Operador, Hotel, Guia, Ciudad, Basico, Opcional
from .models import TipoMomento, TipoRemitente, TipoViaContacto, TipoCausa, TipoPagador
from .models import IncidenciaCamposComunes
from .models import IncidenciaGuia, IncidenciaTransferista, IncidenciaOpcional
from .models import IncidenciaGeneral
from .models import TipoTransferistaIncidencia, TipoTransferistaPunto#, TipoTransferistaRazon
from .models import TipoOpcionalIncidencia, TipoOtroIncidencia, IncidenciaItinerario
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
        # init del query
        self.fields["operador"].queryset = Operador.objects.filter(is_active=True).order_by("nombre")

#   ╔═════════════╗
#   ║ Incidencias ║
#   ╚═════════════╝
class IncidenciaCamposComunesForm(forms.Form):
    """Formulario de captura de datos para los campos comunes que ha de introducir el usuario"""
    momento = forms.ModelChoiceField(
        label="Momento del viaje",
        queryset=TipoMomento.objects.none(),  # placeholder temporal
        empty_label="---------",
        required=True,
    )
    remitente = forms.ModelChoiceField(
        label="Remitente",
        queryset=TipoRemitente.objects.none(),
        empty_label="---------",
        required=True,
    )
    via = forms.ModelChoiceField(
        label="Vía de contacto",
        queryset=TipoViaContacto.objects.none(),
        empty_label="---------",
        required=True,
    )
    causa = forms.ModelChoiceField(
        label="Causa",
        queryset=TipoCausa.objects.none(),
        empty_label="---------",
        required=True,
    )
    pagador = forms.ModelChoiceField(
        label="Pagador",
        queryset=TipoPagador.objects.none(),
        empty_label="---------",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["momento"].queryset = TipoMomento.objects.all().order_by("id")
        self.fields["remitente"].queryset = TipoRemitente.objects.all().order_by("id")
        self.fields["via"].queryset = TipoViaContacto.objects.all().order_by("id")
        self.fields["pagador"].queryset = TipoPagador.objects.all().order_by("id")
        self.fields["causa"].queryset = TipoCausa.objects.all().order_by("id")

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
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
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
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["basico"].queryset = Basico.objects.all().order_by("nombre")
        self.fields["origen"].queryset = Ciudad.objects.all().order_by("nombre")
        self.fields["destino"].queryset = Ciudad.objects.all().order_by("nombre")

class IncidenciaHotelForm(IncidenciaCamposComunesForm):
    hotel = forms.ModelChoiceField(
        queryset=Basico.objects.none(),
        label="Hotel",
        required=True,
        empty_label="Nombre del hotel",
    )
    # Tipos de incidencia
    habitacion = forms.BooleanField(label="ROOM", required=False, initial=False)
    ubicacion = forms.BooleanField(label="UBICACION", required=False, initial=False)
    reservation = forms.BooleanField(label="RESERVE", required=False, initial=False)
    restaurante = forms.BooleanField(label="RESTAURANT", required=False, initial=False)
    otro = forms.BooleanField(label="OTHER", required=False, initial=False)

    field_order = [
        "hotel",
        "habitacion", "ubicacion", "reservation", "restaurante", "otro",
        # Campos Comunes
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hotel"].queryset = Hotel.objects.all().order_by("nombre")

class IncidenciaTransferistaForm(IncidenciaCamposComunesForm):
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        label="Ciudad",
        required=True,
        empty_label="---------",)
    incidencia = forms.ModelChoiceField(
        queryset=TipoTransferistaIncidencia.objects.none(),
        label="Incidencia",
        required=True,
        empty_label="---------",)
    punto = forms.ModelChoiceField(
        queryset=TipoTransferistaPunto.objects.none(),
        label="Punto",
        required=True,
        empty_label="---------",)
    #razon = forms.ModelChoiceField(
    #    queryset=TipoTransferistaRazon.objects.none(),
    #    label="Razón",
    #    required=True,
    #    empty_label="---------",)

    field_order = [
        "ciudad", "incidencia", "punto",# "razon",
        # Campos Comunes
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ciudad"].queryset = Ciudad.objects.all().order_by("nombre")
        self.fields["incidencia"].queryset = TipoTransferistaIncidencia.objects.all().order_by("id")
        self.fields["punto"].queryset = TipoTransferistaPunto.objects.all().order_by("id")
        #self.fields["razon"].queryset = TipoTransferistaRazon.objects.all().order_by("id")

class IncidenciaOpcionalForm(IncidenciaCamposComunesForm):
    opcional = forms.ModelChoiceField(
        queryset=Opcional.objects.none(),
        label="Opcional",
        required=True,
        empty_label="Selecciona una ciudad",)
    
    inc_no_realizado = forms.BooleanField(label="NO_REALIZADO", required=False, initial=False)
    inc_devolucion = forms.BooleanField(label="DEVOLUCIÓN", required=False, initial=False)
    inc_pack = forms.BooleanField(label="GUÍA_LOCAL/BUS/PROVEEDOR", required=False, initial=False)
    inc_otros = forms.BooleanField(label="ROOM", required=False, initial=False)
    #incidencia = forms.ModelChoiceField(
    #    label="Incidencia",
    #    queryset=TipoOpcionalIncidencia.objects.none(),
    #    empty_label="---------",
    #    required=True,
    #)

    field_order = [
        "opcional", "inc_no_realizado", "inc_devolucion", "inc_pack", "inc_otros", 
        # Campos Comunes
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opcional"].queryset = Opcional.objects.all().order_by("nombre")

class IncidenciaOtroForm(IncidenciaCamposComunesForm):
    incidencia = forms.ModelChoiceField(
        label="Incidencia",
        queryset=TipoOtroIncidencia.objects.none(),
        empty_label="---------",
        required=True,
    )

    field_order = [
        "incidencia",
        # Campos Comunes
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["incidencia"].queryset = TipoOtroIncidencia.objects.all().order_by("nombre")

class IncidenciaGeneralForm(IncidenciaCamposComunesForm):
    inc_personal = forms.BooleanField(label="PERSONAL", required=False, initial=False)
    inc_seguro = forms.BooleanField(label="SEGURO", required=False, initial=False)
    inc_otros = forms.BooleanField(label="OTROS", required=False, initial=False)

    field_order = [
        "inc_personal", "inc_seguro", "inc_otros",
        # Campos Comunes
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
    ]

class IncidenciaItinerarioForm(IncidenciaCamposComunesForm):
    ciudad = forms.ModelChoiceField(
        label="Ciudad",
        queryset=Ciudad.objects.none(),
        empty_label="---------",
        required=True,
    )

    inc_itinerario = forms.BooleanField(label="ITINERARIO", required=False, initial=False)
    inc_entradas = forms.BooleanField(label="ENTRADAS", required=False, initial=False)
    inc_billetes = forms.BooleanField(label="BILLETES", required=False, initial=False)
    inc_comidas = forms.BooleanField(label="COMIDAS", required=False, initial=False)
    inc_guia_local = forms.BooleanField(label="GUIA_LOCAL", required=False, initial=False)

    field_order = [
        "ciudad",
        "inc_itinerario", "inc_entradas", "inc_billetes", "inc_guia_local", "inc_comidas",
        # Campos Comunes
        "momento", "remitente", "via", "causa", "pagador", "importe", "comentario",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ciudad"].queryset = Ciudad.objects.all().order_by("nombre")


