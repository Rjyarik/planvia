from fastapi import FastAPI
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Здесь будут добавлены маршруты API