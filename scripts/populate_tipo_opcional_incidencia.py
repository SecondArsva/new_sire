# scripts/populate_tipo_opcional_incidencia.py

# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_tipo_opcional_incidencia import populate_tipo_opcional_incidencia, RAW_DATA
#         populate_tipo_opcional_incidencia(RAW_DATA)

from django.db import transaction

RAW_DATA = """
No realizado
Calidad del servicio
Impago
"""


@transaction.atomic
def populate_tipo_opcional_incidencia(raw_data):
    from core.models import TipoOpcionalIncidencia   # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoOpcionalIncidencia.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creada incidencia de opcional '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: incidencia de opcional '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creadas={created}, saltados={skipped}")
