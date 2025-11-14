# scripts/populate_tipo_transferista_punto.py

# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_tipo_transferista_punto import populate_tipo_transferista_punto, RAW_DATA
#         populate_tipo_transferista_punto(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Aeropuerto / Hotel
Hotel / Aeropuerto
Terminal de buses / Hotel
Hotel / Terminal de buses
Hotel / Hotel
Estación de tren / Hotel
Hotel / Estación de tren
Puerto marítimo / Hotel
Hotel / Puerto marítimo
"""


@transaction.atomic
def populate_tipo_transferista_punto(raw_data):
    from core.models import TipoTransferistaPunto   # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoTransferistaPunto.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creado tipo punto transferista '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: tipo punto transferista '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
