from database.database import init_db, SessionLocal
from database.models import User
# from database.security import get_password_hash

from auth.auth_utils import hash_password

# 1. Genereer de veilige hash
NIEUW_WACHTWOORD = "martijn"
gehashte_wachtwoord = hash_password(NIEUW_WACHTWOORD)

nieuwe_gebruiker = User(
    # email="martijn.guys@gmail.com",  # Gebruik je eigen e-mail
    username="martijn",
    hashed_password=gehashte_wachtwoord,
)

# 3. Open de database sessie
db = SessionLocal()

# 4. Voeg de gebruiker toe en commit de transactie
db.add(nieuwe_gebruiker)
db.commit()
db.refresh(nieuwe_gebruiker)  # Optioneel: verversen
db.close()

print(f"Nieuwe gebruiker '{nieuwe_gebruiker.username}' succesvol aangemaakt.")
