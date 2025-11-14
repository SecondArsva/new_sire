# scripts/populate_hotel.py

# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_hotel import populate_hotel, RAW_DATA
#         populate_hotel(RAW_DATA)

from django.db import transaction

RAW_DATA = """
Gran Madrid - Madrid
Centro Madrid - Madrid
Princesa Ana - Barcelona
Mar Azul - Barcelona
Río Guadalquivir - Sevilla
Playa Dorada - Valencia
Louvre Palace - Paris
Eiffel View - Paris
Roma Centro - Roma
Coliseo Imperial - Roma
"""


@transaction.atomic
def populate_hotel(raw_data):
    from core.models import Hotel, Ciudad  # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        # Separar por " - "
        if " - " not in line:
            print(f"Línea {lineno}: formato inválido, espero 'Hotel - Ciudad' -> {line!r}")
            skipped += 1
            continue

        nombre_hotel, nombre_ciudad = [x.strip() for x in line.split(" - ", 1)]

        # Buscar la ciudad
        try:
            ciudad = Ciudad.objects.get(nombre=nombre_ciudad)
        except Ciudad.DoesNotExist:
            print(f"Línea {lineno}: ciudad '{nombre_ciudad}' no existe. Hotel '{nombre_hotel}' saltado.")
            skipped += 1
            continue

        # Crear o saltar hotel
        obj, was_created = Hotel.objects.get_or_create(
            nombre=nombre_hotel,
            ciudad=ciudad,
        )

        if was_created:
            print(f"Línea {lineno}: creado hotel '{nombre_hotel}' en '{nombre_ciudad}'")
            created += 1
        else:
            print(f"Línea {lineno}: hotel '{nombre_hotel}' en '{nombre_ciudad}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
