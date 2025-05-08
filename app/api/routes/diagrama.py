# app/api/routes/diagrama.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.application.use_cases.crear_diagrama import CrearDiagramaUseCase
from app.application.use_cases.generar_desde_codigo import GenerarDiagramaDesdeCodigoUseCase
from app.infrastructure.repositories.diagrama_inmemory import DiagramaInMemoryRepository

router = APIRouter()

class DiagramaInput(BaseModel):
    nombre: str
    contenido_plantuml: str
    proyecto_id: str
    usuario_id: str

class CodigoFuenteInput(BaseModel):
    codigo: str

crear_use_case = CrearDiagramaUseCase(DiagramaInMemoryRepository())
generar_use_case = GenerarDiagramaDesdeCodigoUseCase()

@router.post("/diagramas")
def crear_diagrama(data: DiagramaInput):
    diagrama = crear_use_case.ejecutar(
        nombre=data.nombre,
        contenido=data.contenido_plantuml,
        proyecto_id=data.proyecto_id,
        usuario_id=data.usuario_id
    )
    return {"id": diagrama.id, "nombre": diagrama.nombre}

@router.post("/generar-diagrama")
def generar_diagrama(data: CodigoFuenteInput):
    uml = generar_use_case.ejecutar(data.codigo)
    return {"uml": uml}