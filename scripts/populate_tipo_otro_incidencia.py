# scripts/populate_tipo_otro_incidencia.py

# FORMATO RAW_DATA:
#   Un nombre por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_tipo_otro_incidencia import populate_tipo_otro_incidencia, RAW_DATA
#         populate_tipo_otro_incidencia(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Causa médica
Robo / hurto
Objeto perdido / olvidado
Otro
"""


@transaction.atomic
def populate_tipo_otro_incidencia(raw_data):
    from core.models import TipoOtroIncidencia

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        nombre = line.strip()
        if not nombre or nombre.startswith("#"):
            continue

        obj, was_created = TipoOtroIncidencia.objects.get_or_create(nombre=nombre)

        if was_created:
            print(f"Línea {lineno}: creado tipo 'Otro' de incidencia → '{nombre}'")
            created += 1
        else:
            print(f"Línea {lineno}: tipo 'Otro' '{nombre}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
