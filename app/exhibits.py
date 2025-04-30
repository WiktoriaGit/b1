from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Exhibit
import cloudinary
import cloudinary.uploader

router = APIRouter()

# Konfiguracja Cloudinary 
#-----------------------------------
cloudinary.config(
    cloud_name="dsqktogv8",
    api_key="792813387329258",
    api_secret="D1fB7m2Dh4UyBTjee0td4Vi1rYc",
    secure=True
)


# Endpoint do tworzenia nowego eksponatu
#-----------------------------------
@router.post("/exhibit/")
def create_exhibit(
    title: str = Form(...),
    description: str = Form(""),
    model: str = Form(...),  
    db: Session = Depends(get_db)
):
    # Walidacja: sprawdź czy to link do .glb
    if not model.endswith(".glb"):
        raise HTTPException(400, "Model musi być linkiem do pliku .glb")

    # Utworzenie obiektu w bazie
    exhibit = Exhibit(title=title, description=description, image_path=model)
    db.add(exhibit)
    db.commit()
    db.refresh(exhibit)

    return {
        "id": exhibit.id,
        "title": exhibit.title,
        "description": exhibit.description,
        "model": exhibit.image_path
    }



# Endpoint do pobierania pojedynczego eksponatu
#-----------------------------------
@router.get("/exhibit/{exhibit_id}")
def get_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).get(exhibit_id)
    if not exhibit:
        raise HTTPException(404, "Nie znaleziono eksponatu.")
    
    return {
        "id": exhibit.id,
        "title": exhibit.title,
        "description": exhibit.description,
        "model_path": exhibit.image_path
    }


# Endpoint do listowania wszystkich eksponatów
#-----------------------------------
@router.get("/exhibit_list")
def get_all_exhibits(db: Session = Depends(get_db)):
    exhibits = db.query(Exhibit).all()
    return [
        {
            "id": exhibit.id,
            "title": exhibit.title,
            "description": exhibit.description,
            "model_url": exhibit.image_path  # lub exhibit.model_url jeśli tak się nazywa
        }
        for exhibit in exhibits
    ]



# Endpoint: edycja tytułu, opisu i modelu
#-----------------------------------
@router.put("/exhibit/{exhibit_id}")
def update_exhibit(
    exhibit_id: int,
    title: str = Form(...),
    description: str = Form(...),
    model: str = Form(...),  # ← teraz to jest link (tekst)
    db: Session = Depends(get_db)
):
    exhibit = db.query(Exhibit).get(exhibit_id)
    if not exhibit:
        raise HTTPException(404, "Nie znaleziono eksponatu.")

    # Aktualizacja pól
    exhibit.title = title
    exhibit.description = description
    exhibit.image_path = model  # ← link .glb

    db.commit()
    db.refresh(exhibit)

    return {
        "msg": "Eksponat zaktualizowany",
        "id": exhibit.id,
        "title": exhibit.title,
        "description": exhibit.description,
        "model_url": exhibit.image_path
    }


# Endpoint usuwanie obrazu
#-------------------------------
@router.delete("/exhibit/{exhibit_id}")
def delete_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).get(exhibit_id)
    if not exhibit:
        raise HTTPException(404, "Nie znaleziono eksponatu.")

    db.delete(exhibit)
    db.commit()
    return {"msg": "Eksponat usunięty", "id": exhibit_id}
