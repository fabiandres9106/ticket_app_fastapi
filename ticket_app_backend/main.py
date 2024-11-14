from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from fastapi.staticfiles import StaticFiles
from app.scheduler.scheduler import schedule_emails_for_events
import asyncio
from app.core.config import settings

import logging
logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

# app = FastAPI(debug=settings.debug)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(schedule_emails_for_events())

# Configuración de CORS
origins = [
    "http://localhost:3000",  # Origen del frontend de React en desarrollo
    "http://127.0.0.1:8080",  # Alternativa para localhost
    "https://estudiocajanegra.net",
    "https://www.estudiocajanegra.net",
    "https://api.estudiocajanegra.net:8443",
    "https://api.estudiocajanegra.net"
    # Agrega otros orígenes según sea necesario, como tu dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router)