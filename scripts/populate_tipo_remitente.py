# scripts/populate_tipo_remitente.py

# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_tipo_remitente import populate_tipo_remitente, RAW_DATA
#         populate_tipo_remitente(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Pasajero
Operador
Minorista
Guía
Transferista
Receptivo
Departamento Interno
Otro
"""


@transaction.atomic
def populate_tipo_remitente(raw_data):
    from core.models import TipoRemitente   # ajusta si no está en core

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoRemitente.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creado tipo remitente '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: tipo remitente '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
