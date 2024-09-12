from fastapi import FastAPI, status, Depends
from fastapi.params import Body
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session
from scraper import scraper_ufu
from typing import List
from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
 'http://localhost:3000'
]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=['*'],
 allow_headers=['*']
)
    
@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2

@app.post("/scraper")
def scrape_and_insert(db: Session = Depends(get_db)):
    items = scraper_ufu()
    
    for item in items:
        new_entry = model.MenuNav(
            menuNav=item['menuNav'],
            link=item['link'],
            created_at=item['created_at']
        )
        db.add(new_entry)
    
    db.commit()
    
    return {"status": "Dados inseridos com sucesso!", "data": items}

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int=100):
 mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
 return mensagens