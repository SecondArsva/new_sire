# scripts/populate_opcionales.py
#
# Script para poblar el modelo Opcional a partir de datos CSV
# con separador coma.
#
# FORMATO RAW_DATA:
#   EXCURSION,CIUDAD
#   NOCHE FLAMENCA,Madrid
#   ...
#
# USO (PowerShell, desde la raíz del proyecto):
#   python manage.py shell
#
#   from scripts.populate_opcionales import RAW_DATA, populate_opcionales
#   populate_opcionales(RAW_DATA)

from django.db import transaction
from core.models import Opcional, Ciudad  # ajusta el import si tu app no es "core"


RAW_DATA = """
EXCURSION,CIUDAD
NOCHE FLAMENCA,Madrid
DE FARAONES A REYES,Madrid
NOCHE FLAMENCA CON CENA GR,Madrid
VISITA A TOLEDO ESPECIAL T22,Madrid
SEGOVIA GR,Madrid
VISITA A TOLEDO,Madrid
VISITA A TOLEDO LAND CRUISE,Madrid
EXPERIENCIA DE COMPRAS INOLVIDABLE OUTLET,Madrid
NOCHE FLAMENCA CON CENA,Madrid
ARTISTICA DE SEVILLA VISITA GUIADA A SU CATEDRAL,Sevilla
ESPECTACULO FLAMENCO EN PATIO SEVILLANO,Sevilla
SINTRA CASCAIS Y ESTORIL,Lisboa
TABLAO FLAMENCO ZAMBRA GITANA LOS TARANTOS,Granada
POSTDAM SANSSOUCI Y PASEO EN BARCO POR EL LAGO WANNSEE CAM 2025,Berlín
CAMPO DE CONCENTRACION SACHSENHAUSEN,Berlín
POSTDAM,Berlín
VALSES EN VIENA,Viena
ARTISTICA DE VIENA PALACIO DE SCHONBRUNN Y OPERA GR,Viena
SAGRADA FAMILIA DE ANTONIO GAUDI,Barcelona
PARIS ILUMINADO,París
PASEO POR EL SENA AL ATARDECER ESPECIAL,París
BARRIO LATINO Y CRUCERO POR EL SENA,París
ESPECTACULO PARADIS LATIN CON CENA,París
BARRIO LATINO CRUCERO POR EL SENA Y TORRE MONTPARNASSE,París
ESPECTACULO MOULIN ROUGE SHOW 2300 HRS,París
BATEAUX MOUCHES SENA CAM 2025,París
ESPECTACULO MOULIN ROUGE SHOW 2100 HRS,París
CENA SHOW FOLCLORICA EN ATENAS,Atenas
VALLE DEL TAMESIS Y PUEBLO DE WINDSOR,Londres
TORRE DE LONDRES Y JOYAS DE LA CORONA CAM 2025,Londres
VISITA GUIADA DE LA CIUDAD DE FLORENCIA,Florencia
MUSEOS VATICANOS Y CAPILLA SIXTINA GM,Roma
NAPOLES POMPEYA,Roma
MUSEOS VATICANOS Y CAPILLA SIXTINA,Roma
MUSEOS VATICANOS CAPILLA SIXTINA GR,Roma
MUSEOS VATICANOS Y CAPILLA SIXTINA DIRECTO,Roma
BASILICAS DE ROMA,Roma
ROMA BARROCA UN PASEO POR LAS MAS BELLAS PLAZAS Y FUENTES,Roma
CAPRI DESDE ROMA GR,Roma
ROMA BARROCA GR,Roma
NAPOLES POMPEYA Y CAPRI,Roma
CAPRI DESDE ROMA,Roma
VISITA GUIADA Y TEATRO GRECOROMANO,Taormina
PASEO EN GONDOLAS EN VENECIA,Venecia
PASEO POR LA LAGUNA DE VENECIA,Venecia
PASEO POR LA LAGUNA BURANO,Venecia
ESPECTACULO FADO CON CENA,Oporto
PRAGA ARTISTICA Y PASEO EN BARCO CHARTER,Praga
PRAGA ARTISTICA,Praga
PASEO POR LOS CANALES DE AMSTERDAM CAM 2025,Ámsterdam
VISITA VOLEMDAM Y MARKEN,Ámsterdam
CANALES DE AMSTERDAM,Ámsterdam
FOLKLORE TIROLES CON CENA,Innsbruck
MT TITLIS ETERNAL SNOW AND GLACIER,Zúrich
PASEO EN BARCO POR LAS CATARATAS DEL RHIN,Zúrich
ZURICHRAPPERSWIL,Zúrich
CENA CON ESPECTACULO UNA EXPERIENCIA UNICA,Marrakech
CENA NOUBA GRUPO SAVOY,Marrakech
GLOBO GRUPO 1,Marrakech
CENA DAR SOUKKAR GRUPO SAVOY,Marrakech
GLOBO GRUPO 2,Marrakech
FANTASIA BEREBER,Marrakech
EXCURSION EN 4X4 POR DESIERTO DEL SAHARA,Erfoud
CRUCERO POR EL DANUBIO Y BUDAPEST ILUMINADO,Budapest
CENA MAGIAR BUDAPEST T24,Budapest
CENA MAGIAR BUDAPEST,Budapest
MINAS DE SAL DE WIEILICZKA,Cracovia
BARRIO JUDIO CAM 2025,Cracovia
MUSEO VASA Y AYUNTAMIENTO CAM 2025,Estocolmo
AYUNTAMIENTO Y BUQUE REAL VASA,Estocolmo
UPPSALA Y SIGTUNA CAM 2025,Estocolmo
MUSEO FRAM Y TRAMPOLIN OLIMPICO,Oslo
MUSEOS DE OSLO FRAM Y KON TIKI CAM 2025,Oslo
VISITA HISTORICA,Estambul
VISITA PARTE ASIATICA,Estambul
MUSEO DEL TITANIC CAM 2025,Dublín
CATEDRAL DE SAN PATRICIO Y DUBLIN A PIE,Dublín
IGLESIA ST PATRICK CAM,Dublín
GUINESS STOREHOUSE CAM 2025,Dublín
VISITA DE CAPRI CAM 2025,Nápoles
ISLA DE CAPRI,Salerno
NAVEGACION POR PUNTA DE LA PIEDAD Y SUS CUEVAS,Albufeira
NOCHE TURCA,Capadocia
PASEO EN GLOBO,Capadocia
VISITA CASSIS Y BODEGA CAM 2025,Marsella
EXCURSION A LAS ISLAS BORROMEAS,Verona
CRUCERO LAGO 4 CANTONES Y MONTE RIGI,Lucerna
LAGO DE LOS 4 CANTONES EN CATAMARAN,Lucerna
CIUDAD DE YORK CAM 2025,Liverpool
CRUCERO PANORAMICO NY,Nueva York
CATARATAS DE MONTMORENCY JARABE DE ARCE CASA DE AZUCAR,Quebec
CANADIAN NATIONAL TOWER,Toronto
TOUR PANORMICO DE CATARATAS DEL NIGARA EN HELICOPTERO,Toronto
TOUR WASHINGTON DE NOCHE,Washington
SUBIDA AL AIGUILLE EN CHAMONIX,Ginebra
VISITA AL PUEBLO DE APPENZELL,Feldkirch
PASEO EN AVIONETA SOBREVOLANDO EL GRAND CANYON,Flagstaff
PASEO EN HELICOPTERO SOBREVOLANDO EL GRAND CANYON,Flagstaff
VISITA NOCTURNA EN LAS VEGAS,Las Vegas
VISITA NOCTURNA EN LAS VEGAS VAN,Las Vegas
GOLDEN GATE BRIDGE Y SAUSALITO,San Francisco
GOLDEN GATE BRIDGE Y SAUSALITO VAN,San Francisco
TRASLADO NOCTURNO A PIER 39 TREASURE ISLAND VAN,San Francisco
PALACIO DE LOS PAPAS CAM 2025,Avignon
TOULOUSE MEDIEVAL CAM 2025,Toulouse
PASEO EN GONDOLAS EN VENECIA PADUA,Padua
CIUDAD DE YORK,Manchester
TREN DE FLAM 2025 CAM2025,Laerdal
""".strip()


def populate_opcionales(raw_data: str) -> None:
    created = 0
    skipped = 0

    with transaction.atomic():
        for raw_line in raw_data.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            # Saltar la cabecera
            if line.upper().startswith("EXCURSION,CIUDAD"):
                continue

            try:
                nombre_excursion, nombre_ciudad = [
                    part.strip() for part in line.split(",", 1)
                ]
            except ValueError:
                print(f"Línea inválida (sin coma o mal formada): {raw_line!r}")
                skipped += 1
                continue

            if not nombre_excursion or not nombre_ciudad:
                print(f"Línea inválida (faltan datos): {raw_line!r}")
                skipped += 1
                continue

            try:
                ciudad = Ciudad.objects.get(nombre__iexact=nombre_ciudad)
            except Ciudad.DoesNotExist:
                print(
                    f"Ciudad no encontrada: {nombre_ciudad!r}. "
                    f"Se omite la excursión {nombre_excursion!r}"
                )
                skipped += 1
                continue

            obj, was_created = Opcional.objects.get_or_create(
                nombre=nombre_excursion,
                ciudad=ciudad,
            )

            if was_created:
                created += 1
            else:
                print(f"Ya existía: {obj.nombre} ({ciudad.nombre})")
                skipped += 1

    print(f"Opcionales creados: {created}")
    print(f"Opcionales saltados/omitidos: {skipped}")
