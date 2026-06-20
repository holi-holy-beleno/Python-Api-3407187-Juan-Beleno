from fastapi import APIRouter, HTTPException, status
from modelos.facturas import Factura, FacturaCrear, FacturaEditar
from enrutadores.clientes import lista_clientes 

router = APIRouter(prefix="/facturas", tags=["Facturas"])

lista_facturas = []

@router.get("")
async def listar_facturas():
    return {"Facturas": lista_facturas}

@router.get("/{factura_id}")
async def consultar_factura(factura_id: int):
    for objeto_factura in lista_facturas:
        if objeto_factura.id == factura_id:
            return {"Factura": objeto_factura}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La factura con ID {factura_id} no existe."
    )

@router.post("")
async def crear_factura(cliente_id: int, datos_factura : FacturaCrear):
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break
            
    if cliente_encontrado is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con ID {cliente_id} no existe."
        )
        
    id_factura = len(lista_facturas) + 1
    
    factura_dict = datos_factura.model_dump()
    factura_validada = Factura(**factura_dict)
    
    factura_validada.id = id_factura
    factura_validada.cliente = cliente_encontrado
    
    lista_facturas.append(factura_validada)
    return factura_validada

@router.put("/{id}")
async def editar_factura(id: int, datos_actualizados: FacturaEditar): 
    for i, objeto_factura in enumerate(lista_facturas):
        if objeto_factura.id == id:
            datos_dict = datos_actualizados.model_dump()
            factura_validada = Factura(**datos_dict)
            factura_validada.id = id
            lista_facturas[i] = factura_validada
            return factura_validada
    raise HTTPException(status_code=400, detail=f"La factura con ID {id} no existe.")

@router.delete("/{id}")
async def eliminar_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            lista_facturas.remove(factura)
            return {"mensaje": "La factura fue eliminada con exito"}
    raise HTTPException(status_code=400, detail=f"La factura con ID {id} no existe.")