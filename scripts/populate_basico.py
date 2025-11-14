# scripts/populate_basico.py

# FORMATO RAW_DATA:
#   Un código por línea
#
# POWERSHELL:
#   - abrir la shell:
#         python manage.py shell
#
#   - ejecutar dentro de la shell:
#         from scripts.populate_basico import populate_basico, RAW_DATA
#         populate_basico(RAW_DATA)

from django.db import transaction

RAW_DATA = """
VUASTOKPEK24
VUBEIRAMM24
VULONBER24
VUMXHABMEX24
VUMXLSTCR24
VUMXMERMEX24
VUMXMEXHAB24
VUORAMACAI24
VUORCAILUX24
VUORCAIRESTA24
VUORCAPAMAN24
VUORCASWESTA24
VUORESTATELAV24
VUORKERAMA24
VUPALROM24
VUROMAD24
VUROMATE24
VUROMPAL24
VUSACHILAX24
VUSALAXCHI24
VUSALAXNY24
VUSANYLAX24
VUSATORLAX24
VUSAVEGCHI24
VUSAVEGLAX24
VUSOFEST24
VUVENPAL24
VUVENPAR24
VUVIENMO24
"""


@transaction.atomic
def populate_basico(raw_data):
    from core.models import Basico   # ajusta si está en otra app

    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        codigo = line.strip()
        if not codigo or codigo.startswith("#"):
            continue

        obj, was_created = Basico.objects.get_or_create(nombre=codigo)

        if was_created:
            print(f"Línea {lineno}: creado básico '{codigo}'")
            created += 1
        else:
            print(f"Línea {lineno}: básico '{codigo}' ya existe, se salta")
            skipped += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")
