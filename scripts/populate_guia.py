# scripts/populate_guia.py

# FORMATO RAW_DATA (un guía por línea):
#   nombre$apellido1
#   nombre$apellido1$apellido2
#   admite nombres y apellidos compuestos al usar el "$" como separador.
#
#   Ejemplo:
#       Harrison$Ford$Focus
#       Indiana$Jones
#       Han$Solo
#       Rick$Deckard
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_guia import populate_guia, RAW_DATA
#         populate_guia(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Sin$Especificar
Harrison$Ford$Focus
Indiana$Jones
Han$Solo
Rick$Deckard
"""


@transaction.atomic
def populate_guia(raw_data):
    from core.models import Guia   # ajusta si no está en core

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Partes separadas por dólar ($)
        parts = [p.strip() for p in line.split("$")]

        if len(parts) < 2 or len(parts) > 3:
            print(f"Línea {lineno}: formato inválido, espero 'nombre$apellido1[$apellido2]' -> {line!r}")
            skipped += 1
            continue

        nombre = parts[0]
        apellido1 = parts[1]
        apellido2 = parts[2] if len(parts) == 3 else ""   # 👉 apellido2 vacío si no viene

        if not nombre or not apellido1:
            print(f"Línea {lineno}: nombre o primer apellido vacío -> {line!r}")
            skipped += 1
            continue

        obj, was_created = Guia.objects.get_or_create(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
        )

        etiqueta = f"{nombre} {apellido1}" + (f" {apellido2}" if apellido2 else "")

        if was_created:
            print(f"Línea {lineno}: creado guía '{etiqueta}'")
            created += 1
        else:
            print(f"Línea {lineno}: guía '{etiqueta}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
