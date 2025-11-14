# scripts/populate_paises.py

import os
import django
from django.db import transaction

# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell de Python:
#         from scripts.populate_pais import populate_pais, RAW_DATA
#         populate_pais(RAW_DATA)
#
#   - si quieres volver a ejecutar después de editar RAW_DATA:
#         reload()
#         from scripts.populate_pais import populate_pais, RAW_DATA
#         populate_pais(RAW_DATA)

def django_setup_if_needed():
    if not django.apps.apps.ready:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_sire.settings")
        django.setup()


RAW_DATA = """
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
def populate_pais():
    from core.models import Pais  # ajusta si tu modelo está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(RAW_DATA.splitlines(), start=1):
        nombre = line.strip()

        # Ignorar líneas vacías o comentarios
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = Pais.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creado país '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: ya existía '{nombre}', se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")

if __name__ == "__main__":
    django_setup_if_needed()
    populate_pais()
