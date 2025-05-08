# # app/api/routes/generar_diagrama_desde_codigo.py
# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.application.services.csharp_to_plantuml_converter import CSharpToPlantUMLConverter

# router = APIRouter()

# class CodigoFuenteInput(BaseModel):
#     codigo_fuente: str

# @router.post("/generar-diagrama")
# def generar_diagrama_desde_codigo(data: CodigoFuenteInput):
#     converter = CSharpToPlantUMLConverter()
#     plantuml = converter.convertir(data.codigo_fuente)
#     return {"plantuml": plantuml}



# # app/api/routes/generar_diagrama_desde_codigo.py
# from fastapi import APIRouter, HTTPException, Query
# from typing import List
# from app.application.use_cases.generar_desde_codigo import GenerarDiagramaDesdeCodigoUseCase

# router = APIRouter(
#     prefix="/diagramas",
#     tags=["diagramas"]
# )

# @router.post("/generar", summary="Genera diagramas UML desde código fuente")
# async def generar_diagrama(
#     codigo: str,
#     lenguaje: str = Query("csharp", description="Lenguaje del código fuente", enum=["csharp", "java", "python"]),
#     diagramas: List[str] = Query(
#         ["class"], 
#         description="Tipos de diagramas a generar",
#         enum=["class", "sequence", "usecase"]  # Extiende según necesidades
#     )
# ):
#     try:
#         use_case = GenerarDiagramaDesdeCodigoUseCase()
#         resultados = use_case.ejecutar(
#             codigo_fuente=codigo,
#             lenguaje=lenguaje,
#             diagramas_solicitados=diagramas
#         )
        
#         return {
#             "success": True,
#             "data": resultados,
#             "meta": {
#                 "lenguaje": lenguaje,
#                 "diagramas_generados": list(resultados.keys())
#             }
#         }
#     except ValueError as e:
#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error interno al generar diagramas: {str(e)}"
#         )





# # app/api/routes/generar_diagrama_desde_codigo.py
# from fastapi import APIRouter, HTTPException, Query, Body
# from typing import List, Union
# from pydantic import BaseModel
# from app.application.use_cases.generar_desde_codigo import GenerarDiagramaDesdeCodigoUseCase

# router = APIRouter(prefix="/diagramas", tags=["diagramas"])

# # Modelo para compatibilidad con versión anterior
# class CodigoFuenteInput(BaseModel):
#     codigo_fuente: str
#     lenguaje: str = "csharp"
#     diagramas: List[str] = ["class"]

# @router.post("/generar", summary="Genera diagramas UML desde código fuente")
# @router.post("/generar-diagrama", deprecated=True)  # Mantiene compatibilidad
# async def generar_diagrama(
#     codigo: str = Query(None, description="Código fuente"),
#     lenguaje: str = Query("csharp", enum=["csharp", "java", "python"]),
#     diagramas: List[str] = Query(["class"], enum=["class", "sequence"]),
#     # Soporta también el formato JSON antiguo
#     body_data: CodigoFuenteInput = Body(None)
# ):
#     try:
#         # Combina parámetros de query y body
#         final_codigo = codigo if codigo is not None else (body_data.codigo_fuente if body_data else None)
#         if final_codigo is None:
#             raise ValueError("Código fuente requerido")

#         use_case = GenerarDiagramaDesdeCodigoUseCase()
#         resultados = use_case.ejecutar(
#             codigo_fuente=final_codigo,
#             lenguaje=lenguaje,
#             diagramas_solicitados=diagramas
#         )
        
#         return {
#             "success": True,
#             "plantuml": resultados.get("class"),  # Compatibilidad
#             "data": resultados,  # Nuevo formato
#             "meta": {
#                 "lenguaje": lenguaje,
#                 "diagramas_generados": list(resultados.keys())
#             }
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# app/api/routes/generar_diagrama_desde_codigo.py
from fastapi import APIRouter, HTTPException, Body
from typing import List
from pydantic import BaseModel
from app.application.use_cases.generar_desde_codigo import GenerarDiagramaDesdeCodigoUseCase

router = APIRouter(prefix="/api/diagramas", tags=["diagramas"])  # Cambiado a /api/diagramas

class DiagramaRequest(BaseModel):
    codigo: str
    lenguaje: str = "csharp"
    diagramas: List[str] = ["class"]

@router.post("/generar", summary="Genera diagramas UML desde código fuente")
async def generar_diagrama(
    request: DiagramaRequest = Body(...)  # Solo Body, no Query params
):
    try:
        use_case = GenerarDiagramaDesdeCodigoUseCase()
        resultados = use_case.ejecutar(
            codigo_fuente=request.codigo,
            lenguaje=request.lenguaje,
            diagramas_solicitados=request.diagramas
        )
        
        return {
            "success": True,
            "plantuml": resultados.get("class"),  # Compatibilidad con frontend antiguo
            "data": resultados,  # Nuevo formato
            "meta": {
                "lenguaje": request.lenguaje,
                "diagramas_generados": list(resultados.keys())
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))