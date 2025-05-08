# app/application/use_cases/crear_diagrama.py
from uuid import uuid4
from app.domain.entities import Diagrama
from app.domain.repositories import DiagramaRepository

class CrearDiagramaUseCase:
    def __init__(self, diagrama_repo: DiagramaRepository):
        self.diagrama_repo = diagrama_repo

    def ejecutar(self, nombre: str, contenido: str, proyecto_id: str, usuario_id: str) -> Diagrama:
        diagrama = Diagrama(
            id=str(uuid4()),
            nombre=nombre,
            contenido_plantuml=contenido,
            proyecto_id=proyecto_id,
            creado_por=usuario_id
        )
        self.diagrama_repo.guardar(diagrama)
        return diagrama
