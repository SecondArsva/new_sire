# scripts/populate_tipo_pagador.py

# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_tipo_pagador import populate_tipo_pagador, RAW_DATA
#         populate_tipo_pagador(RAW_DATA)

from django.db import transaction

RAW_DATA = """
EMV
PAX
Agencia
Nadie
"""


@transaction.atomic
def populate_tipo_pagador(raw_data):
    from core.models import TipoPagador   # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoPagador.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creado tipo pagador '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: tipo pagador '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
