# app/application/use_cases/generar_desde_codigo.py
# from app.application.services.csharp_to_plantuml_converter import CSharpToPlantUMLConverter

# class GenerarDiagramaDesdeCodigoUseCase:
#     def __init__(self):
#         self.converter = CSharpToPlantUMLConverter()

#     def ejecutar(self, codigo_fuente: str) -> str:
#         return self.converter.convert(codigo_fuente)

# app/application/use_cases/generar_desde_codigo.py
from typing import Dict, List
from app.application.services.diagram_factory import DiagramFactory
from app.application.services.diagram_builder import DiagramBuilder

class GenerarDiagramaDesdeCodigoUseCase:
    def __init__(self, factory=None, builder=None):
        self.factory = factory or DiagramFactory()
        self.builder = builder or DiagramBuilder(self.factory)

    def ejecutar(
        self,
        codigo_fuente: str,
        lenguaje: str,
        diagramas_solicitados: List[str] = None
    ) -> Dict[str, str]:
        
        if not diagramas_solicitados:
            diagramas_solicitados = ['class']  # Valor por defecto
            
        return self.builder.build_diagrams(
            code=codigo_fuente,
            language=lenguaje,
            diagram_types=diagramas_solicitados
        )

