# scripts/populate_pais.py

# FORMATO RAW_DATA:
#   Un país por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_pais import populate_pais, RAW_DATA
#         populate_pais(RAW_DATA)

from django.db import transaction

RAW_DATA = """
None
España
Francia
Italia
Portugal
Alemania
Reino Unido
Andorra
Marruecos
Egipto
Turquía
Estados Unidos
México
Brasil
Argentina
Chile
Perú
"""


@transaction.atomic
def populate_pais(raw_data):
    from core.models import Pais   # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = Pais.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creado país '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: país '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
