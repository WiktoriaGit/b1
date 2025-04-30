#sprawdza dane i tworzy ich szablony
from pydantic import BaseModel

#szablon do tworzenia użytkownika
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"
    
#szablon użytkownika do wysyłania    
class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True #pozwala fastapi czytac z obiektów bazy danych


#szablon eksponatu do wysyłania
class ExhibitOut(BaseModel):
    id: int
    title: str
    description: str
    image_path: str  

    class Config:
        orm_mode = True

