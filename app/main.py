from fastapi import FastAPI #tworzy aplikacje
from fastapi.middleware.cors import CORSMiddleware #łączy frontend z backendem
from fastapi.staticfiles import StaticFiles #do obsługi folderu z plikami .glb lokalnie
from fastapi.responses import StreamingResponse #do zwracania kodów QR

from .users import router as users_router
from .exhibits import router as exhibit_router
from .database import engine
from . import models
from . import auth

import os
import qrcode
import io

# Tworzenie tabel w bazie danych
#------------------------------
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rejestracja routerów
#------------------------------
app.include_router(users_router)
app.include_router(exhibit_router)


# CORS - komunikacja frontendu Vercel + lokalnie z backendem
#------------------------------
origins = [
    "http://localhost:8080", # lokalny frontend (np. podczas testów)
    "https://wm-frontend-one.vercel.app"  # frontend na Vercelu
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wm-frontend-one.vercel.app"],  # komu pozwalamy
    allow_credentials=True, # pozwól na ciasteczka/tokeny
    allow_methods=["*"],    # pozwól na wszystkie metody (GET, POST, itd.)
    allow_headers=["*"],    # pozwól na dowolne nagłówki (np. Authorization)
)


#Endpoint do generowania kodów QR
#------------------------------
@app.get("/qrcode/{exhibit_id}")
def generate_qr(exhibit_id: int):
    base_url = "https://wm-frontend-one.vercel.app/view.html"
    full_url = f"{base_url}?id={exhibit_id}"
    qr_img = qrcode.make(full_url) #biblioteka qrcode do tworzenia obrazków

    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

#  Obsługuje folder, w którym są lokalnie pliki
if not os.path.exists("uploaded_models"):
    os.makedirs("uploaded_models")
    
app.mount("/uploaded_models", StaticFiles(directory="uploaded_models"), name="uploaded_models")
