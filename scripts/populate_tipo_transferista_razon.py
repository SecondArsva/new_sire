# scripts/populate_tipo_transferista_razon.py

# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_tipo_transferista_razon import populate_tipo_transferista_razon, RAW_DATA
#         populate_tipo_transferista_razon(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Flight change
Flight delay
Lost Luggage
Airport Service (Passport control, Luggage pick-up)
PAX Error
TSF Error
Unknown
"""


@transaction.atomic
def populate_tipo_transferista_razon(raw_data):
    from core.models import TipoTransferistaRazon   # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoTransferistaRazon.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creada razón transferista '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: razón transferista '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creadas={created}, saltados={skipped}")
