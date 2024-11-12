from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # Origen del frontend de React en desarrollo
    "http://127.0.0.1:3000",  # Alternativa para localhost
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