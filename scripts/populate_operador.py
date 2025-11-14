# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_operador import populate_operador, RAW_DATA
#         populate_operador(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Europamundo - España
CityTours Travel - España
Francia Viajes - Francia
ItaliaExperience - Italia
PortuRutas - Portugal
GermanWander - Alemania
ParisLuxuryTours - Francia
RomaClassicTours - Italia
"""


@transaction.atomic
def populate_operador(raw_data):
    from core.models import Operador, Pais   # ajusta la app si hace falta

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        # Debe contener " - "
        if " - " not in line:
            print(f"Línea {lineno}: formato inválido, espero 'Operador - Pais' -> {line!r}")
            skipped += 1
            continue

        nombre_operador, nombre_pais = [x.strip() for x in line.split(" - ", 1)]

        # Buscar el país
        try:
            pais = Pais.objects.get(nombre=nombre_pais)
        except Pais.DoesNotExist:
            print(f"Línea {lineno}: país '{nombre_pais}' no existe. Operador '{nombre_operador}' saltado.")
            skipped += 1
            continue

        # Crear o saltar operador
        obj, was_created = Operador.objects.get_or_create(
            nombre=nombre_operador,
            pais=pais
        )

        if was_created:
            print(f"Línea {lineno}: creado operador '{nombre_operador}' ({nombre_pais})")
            created += 1
        else:
            print(f"Línea {lineno}: operador '{nombre_operador}' en '{nombre_pais}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
