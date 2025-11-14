# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_via_contacto import populate_via_contacto, RAW_DATA
#         populate_via_contacto(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Teléfono
Chat
Email
Otro
"""


@transaction.atomic
def populate_tipo_via_contacto(raw_data):
    from core.models import TipoViaContacto   # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoViaContacto.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creada vía de contacto '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: vía de contacto '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
