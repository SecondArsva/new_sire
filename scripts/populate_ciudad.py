# scripts/populate_ciudad.py

# FORMATO RAW_DATA (ciudad $ pais):
#   Ciudad$Pais
#   Ejemplo:
#       Madrid$España
#       Nueva York$Estados Unidos
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar:
#         from scripts.populate_ciudad import populate_ciudad, RAW_DATA
#         populate_ciudad(RAW_DATA)

from django.db import transaction

RAW_DATA = """
None$None
Madrid$España
Barcelona$España
Sevilla$España
Valencia$España
Paris$Francia
Lyon$Francia
Marsella$Francia
Roma$Italia
Milán$Italia
Turín$Italia
"""


@transaction.atomic
def populate_ciudad(raw_data):
    from core.models import Ciudad, Pais   # ajusta la app si es necesario

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Dividir por el separador $
        if "$" not in line:
            print(f"Línea {lineno}: formato inválido → {line!r}. Esperado 'Ciudad$Pais'")
            skipped += 1
            continue

        nombre_ciudad, nombre_pais = [p.strip() for p in line.split("$", 1)]

        if not nombre_ciudad or not nombre_pais:
            print(f"Línea {lineno}: Ciudad o País vacío → {line!r}")
            skipped += 1
            continue

        # Buscar país
        try:
            pais = Pais.objects.get(nombre=nombre_pais)
        except Pais.DoesNotExist:
            print(f"Línea {lineno}: el país '{nombre_pais}' no existe. Ciudad '{nombre_ciudad}' saltada.")
            skipped += 1
            continue

        # Crear ciudad
        obj, was_created = Ciudad.objects.get_or_create(
            nombre=nombre_ciudad,
            pais=pais,
        )

        if was_created:
            print(f"Línea {lineno}: creada ciudad '{nombre_ciudad}' ({nombre_pais})")
            created += 1
        else:
            print(f"Línea {lineno}: ciudad '{nombre_ciudad}' ya existe en '{nombre_pais}', se salta")
            skipped += 1

    print(f"\nResumen: creadas={created}, saltadas={skipped}")
