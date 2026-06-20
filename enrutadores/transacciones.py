from fastapi import APIRouter, HTTPException, status
from modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from enrutadores.facturas import lista_facturas 

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

lista_transacciones = []

@router.get("")
async def listar_transacciones():
    return {"Transacciones": lista_transacciones}

@router.get("/{id}")
async def consultar_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return {"Transaction": transaccion}
    # 3. Cambiado a status para mantener el estándar profesional
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La transacción con ID {id} no existe."
    )

@router.post("")
async def crear_transaccion(factura_id: int, datos_transaccion : TransaccionCrear):
    factura_encontrada = None
    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura
            break
            
    if factura_encontrada is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con ID {factura_id} no existe."
        )
        
    id_transaccion = len(lista_transacciones) + 1
    tx_dict = datos_transaccion.model_dump()
    transaccion_validada = Transaccion(**tx_dict)
    transaccion_validada.id = id_transaccion
    transaccion_validada.factura_id = factura_id
    
    lista_transacciones.append(transaccion_validada)
    factura_encontrada.transacciones.append(transaccion_validada)
    
    return transaccion_validada

@router.put("/{id}")
async def editar_transaccion(id: int, datos_actualizados: TransaccionEditar): 
    for i, objeto_transaccion in enumerate(lista_transacciones):
        if objeto_transaccion.id == id:
            datos_dict = datos_actualizados.model_dump()
            transaccion_validada = Transaccion(**datos_dict)
            transaccion_validada.id = id
            lista_transacciones[i] = transaccion_validada
            return transaccion_validada
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La transacción con ID {id} no existe."
    )

@router.delete("/{id}")
async def eliminar_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            lista_transacciones.remove(transaccion)
            return {"mensaje": "La transacción fue eliminada con exito"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La transacción con ID {id} no existe."
    )