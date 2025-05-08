# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import diagrama, generar_diagrama_desde_codigo

app = FastAPI(title="UML Generator API")

# Permite CORS para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(diagrama.router, prefix="/api")
app.include_router(generar_diagrama_desde_codigo.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API UML Generator activa"}
