from django.contrib.auth import get_user_model
from django.db.models import Q

# Listado de usuarios correspondiente a:
# https://www.europamundo-online.com/Operadores/buscaAgente.asp
# Búsqueda con filtro de E-mail con "attcliente".

# Ejecución: 
# BASH: python manage.py shell < scripts/populate_users.py
# POWERSHELL:
#   - abrir la shell:
#       python manage.py shell
#   - ejecutar:
#       from scripts.populate_users import populate_users, RAW_DATA
#       populate_users(RAW_DATA)

RAW_DATA = """
FERNANDOATT fernando.ayala@europamundo.com
VIRIATT viridiana.rendon@europamundo.com
FELIPEATT felipe.dossantos@europamundo.com
PILARATT pilar.garcia@europamundo.com
# JAVIERATT serviciosenruta@europamundo.com ???
ROSAATT rosa.pego@europamundo.com
AKIOATT akio.morimoto@europamundo.com
# CAMI ???
# FATI ???
FACUNDOL facundo.lind@europamundo.com
"""

COMMON_PASSWORD = "1234"


def populate_users(raw_data):
    User = get_user_model()
    created = 0
    skipped = 0

    for lineno, line in enumerate(raw_data.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) != 2:
            print(f"Línea {lineno}: formato inválido, espero 'USER email' -> {line!r}")
            skipped += 1
            continue

        username, email = parts
        email = email.strip()

        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            print(
                f"Línea {lineno}: ya existe un usuario con ese username o email "
                f"(username={username}, email={email}). No se modifica."
            )
            skipped += 1
            continue

        user = User.objects.create_user(
            username=username,
            email=email,
            password=COMMON_PASSWORD,
        )
        print(f"Línea {lineno}: creado usuario {user.username} ({user.email})")
        created += 1

    print(f"\nResumen: creados={created}, saltados={skipped}")


if __name__ == "__main__":
    populate_users(RAW_DATA)
