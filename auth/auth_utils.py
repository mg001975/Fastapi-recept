from passlib.context import CryptContext

# Initialize the password context (for hashing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Function to verify the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(hashed_password)
    print(plain_password)
    return pwd_context.verify(plain_password, hashed_password)
