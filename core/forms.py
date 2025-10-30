# core/forms.py
from django import forms
# AUTH
from django.contrib.auth.forms import AuthenticationForm    # ╔══════╗
from django.contrib.auth.models import User                 # ║ AUTH ║
from django.contrib.auth import authenticate                # ╚══════╝

from .models import Operador, Hotel
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
class DatosComunesForm(forms.Form):
    # momento
    # remitente
    # via
    # causa
    # extra_payment
    # amount
    importe_euros = forms.IntegerField(
        label="Euros",
        required=True,
        max_value=5,
    )
    importe_centimos = forms.IntegerField(
        label="Centimos",
        required=True,
        max_value=2,
    )
    # commentary
    comentario = forms.CharField(
        label="Comentario",
        max_length=2000,
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Escribe aquí los detalles…",
            "rows": 5,
        }),
    )

#class IncidenciaHotelForm(forms.Form):
#    hotel = forms.ModelChoiceField(
#        queryset=Hotel.objects.none(),
#        label="Hotel",
#        required=True,
#    )
#    incidencia = forms.ModelChoiceField(
#        
#    )
#
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields["hotel"].queryset = Hotel.objects.all()
