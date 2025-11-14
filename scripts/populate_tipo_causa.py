# scripts/populate_tipo_causa.py

# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_tipo_causa import populate_tipo_causa, RAW_DATA
#         populate_tipo_causa(RAW_DATA)

from django.db import transaction

RAW_DATA = """
EMV
PAX
OPERATOR
DMC (Destination Management Company)
UNKNOWN
INFO
CONGRATS
"""


@transaction.atomic
def populate_tipo_causa(raw_data):
    from core.models import TipoCausa   # ajusta si la app es otra

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoCausa.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creado tipo causa '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: tipo causa '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
