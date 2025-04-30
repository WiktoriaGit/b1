from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from .users import router as users_router
from .exhibits import router as exhibit_router
from .database import engine
from . import models
from . import auth

import os
import qrcode
import io

# Tworzenie tabel w bazie danych
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware CORS – musi być *przed* routerami!
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", 
        "https://wm-frontend-one.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestracja routerów
app.include_router(users_router)
app.include_router(exhibit_router)

# Endpoint do generowania kodów QR
@app.get("/qrcode/{exhibit_id}")
def generate_qr(exhibit_id: int):
    base_url = "https://wm-frontend-one.vercel.app/view.html"
    full_url = f"{base_url}?id={exhibit_id}"
    qr_img = qrcode.make(full_url)

    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

# Obsługa folderu z lokalnymi modelami
if not os.path.exists("uploaded_models"):
    os.makedirs("uploaded_models")

app.mount("/uploaded_models", StaticFiles(directory="uploaded_models"), name="uploaded_models")
