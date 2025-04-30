#hasła, tokeny, autoryzacja
from datetime import datetime, timedelta
from jose import jwt, JWTError #biblioteka do tworzenia i sprawdzania tokenów JWT
from passlib.context import CryptContext #bcrypt algorytm do hashowania haseł

# Tajny klucz do podpisywania tokenu
SECRET_KEY = "kluczPodpisDoPorownaniaZjwt"  #pozniej przenies do pliku .env
ALGORITHM = "HS256"   #typ podpisu

# Konfiguracja hashowania haseł (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funkcja: hashowanie hasła 
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Funkcja: weryfikacja hasła
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Funkcja: tworzenie tokenu JWT
def create_token(username: str, role: str, expires_minutes: int = 60) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Funkcja: sprawdzanie tokenu JWT
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": payload["sub"],
            "role": payload["role"]
        }
    except JWTError:
        raise ValueError("Token nieprawidłowy lub wygasł.")
