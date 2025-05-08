from abc import ABC, abstractmethod
from typing import Optional, List
from .entities import Proyecto, Diagrama, Usuario

class ProyectoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, proyecto_id: str) -> Optional[Proyecto]:
        pass

    @abstractmethod
    def guardar(self, proyecto: Proyecto):
        pass

class DiagramaRepository(ABC):
    @abstractmethod
    def guardar(self, diagrama: Diagrama):
        pass

    @abstractmethod
    def obtener_por_id(self, diagrama_id: str) -> Optional[Diagrama]:
        pass

    @abstractmethod
    def obtener_por_proyecto(self, proyecto_id: str) -> List[Diagrama]:
        pass

class UsuarioRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, usuario_id: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass