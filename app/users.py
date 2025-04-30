# app/users.py

from fastapi import APIRouter, HTTPException, status, Depends #endpointy/błędy/kody/uruchomienie innej funkcji
from sqlalchemy.orm import Session #sesja z baza
from fastapi.security import OAuth2PasswordBearer #pobiera token jwt z nagłówka
from fastapi import Form #odebranie danych przesłanych z formularza html

from .database import get_db
from .models import User
from .auth import create_token, decode_token, hash_password, verify_password
from .models import User
from .schemas import UserOut

router = APIRouter()


# Mechanizm OAuth2
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") #Ustawia sposób pobierania tokenu JWT z przeglądarki.

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict: #wyciąga JWT i przekazuje ja do funkcji jako token
    try:
        user_info = decode_token(token) #sprawdzany token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) #jesli token jest zły to wyrzuca błąd
    return user_info #jeśli token jest ok to zwraca username i role


# Endpoint do tworzenia usera
# -----------------------------
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    db: Session = Depends(get_db)
):
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Użytkownik o takiej nazwie już istnieje."
            )

        hashed_pw = hash_password(password)
        new_user = User(username=username, hashed_password=hashed_pw, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role
        }
    except Exception as e:
        print(" BŁĄD:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Coś poszło nie tak przy tworzeniu użytkownika: {str(e)}"
        )



# Endpoint do logowania
# -----------------------------
@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
): #dane z formularza, połączenie z baza
    user = db.query(User).filter(User.username == username).first() #szuka w bazie usera o danej nazwie
    
    if not user: #jeśli nie ma usera
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Niepoprawne dane logowania (brak użytkownika)."
        )

    if not verify_password(password, user.hashed_password): #user jest ale hasło niepoprawne
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Niepoprawne hasło."
        )

    token = create_token(user.username, user.role) #login i hasło ok, tworzy token JWT
    return {
    "token": token,
    "role": user.role
    } #Token trafia do localStorage


# Przykład endpointu chronionego
# -----------------------------
@router.get("/protected")
def protected_endpoint(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Witaj {current_user['username']}, twój endpoint jest chroniony!",
        "role": current_user["role"]
    }
#Endpoint dostępny tylko dla zalogowanych użytkowników (dowolna rola).
#Wystarczy mieć ważny token, by tu wejść.


# Przykład endpointu TYLKO dla admina
# -----------------------------
@router.post("/secret-admin")
def secret_admin_action(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak uprawnień (musisz być adminem)."
        )
    return {"message": "Akcja dostępna tylko dla admina."}


# Przykład endpointu wyswietlanie listy userow
# -----------------------------
@router.get("/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
    
    
#Endpoint do usuwania
#-----------------------------------
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "Użytkownik nie istnieje.")

    db.delete(user)
    db.commit()
    return {"msg": "Użytkownik usunięty", "id": user_id}
