from django.db import transaction

# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar:
#         from scripts.populate_ciudad import populate_ciudad, RAW_DATA
#         populate_ciudad(RAW_DATA)

RAW_DATA = """
Madrid España
Barcelona España
Sevilla España
Valencia España
Paris Francia
Lyon Francia
Marsella Francia
Roma Italia
Milán Italia
Turín Italia
"""

@transaction.atomic
def populate_ciudad(raw_data):
    from core.models import Ciudad, Pais  # Ajusta si tu modelo está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) != 2:
            print(f"Línea {lineno}: formato inválido, espero 'Ciudad Pais' -> {line!r}")
            skipped += 1
            continue

        nombre_ciudad, nombre_pais = parts

        # Buscar el país
        try:
            pais = Pais.objects.get(nombre=nombre_pais)
        except Pais.DoesNotExist:
            print(f"Línea {lineno}: país '{nombre_pais}' no existe. Ciudad '{nombre_ciudad}' saltada.")
            skipped += 1
            continue

        # Crear o saltar ciudad
        obj, was_created = Ciudad.objects.get_or_create(
            nombre=nombre_ciudad,
            pais=pais
        )

        if was_created:
            print(f"Línea {lineno}: creada ciudad '{nombre_ciudad}' en '{nombre_pais}'")
            created += 1
        else:
            print(f"Línea {lineno}: '{nombre_ciudad}' ya existe en '{nombre_pais}', se salta")
            skipped += 1

    print(f"\nResumen: creadas={created}, saltadas={skipped}")
