# app/domain/entities.py
from enum import Enum
from uuid import uuid4
from datetime import datetime
from typing import Optional

class RolProyecto(str, Enum):
    LECTOR = "lector"
    COLABORADOR = "colaborador"
    ADMINISTRADOR = "administrador"

class Usuario:
    def __init__(self, id: str, email: str, nombre: str):
        self.id = id
        self.email = email
        self.nombre = nombre

class Proyecto:
    def __init__(self, id: str, nombre: str, propietario_id: str, uuid_publico: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.propietario_id = propietario_id
        self.uuid_publico = uuid_publico or str(uuid4())

class RolDeUsuarioEnProyecto:
    def __init__(self, usuario_id: str, proyecto_id: str, rol: RolProyecto):
        self.usuario_id = usuario_id
        self.proyecto_id = proyecto_id
        self.rol = rol

class Diagrama:
    def __init__(self, id: str, nombre: str, contenido_plantuml: str, proyecto_id: str, creado_por: str, creado_en: Optional[datetime] = None):
        self.id = id
        self.nombre = nombre
        self.contenido_plantuml = contenido_plantuml
        self.proyecto_id = proyecto_id
        self.creado_por = creado_por
        self.creado_en = creado_en or datetime.utcnow()

class Invitacion:
    def __init__(self, id: str, proyecto_id: str, email_invitado: str, rol_asignado: RolProyecto, estado: str = "pendiente"):
        self.id = id
        self.proyecto_id = proyecto_id
        self.email_invitado = email_invitado
        self.rol_asignado = rol_asignado
        self.estado = estado