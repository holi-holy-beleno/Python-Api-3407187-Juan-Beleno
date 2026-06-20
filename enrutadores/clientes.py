from fastapi import APIRouter, HTTPException, status
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar

router = APIRouter(prefix="/clientes", tags=["Clientes"])

lista_clientes = []

@router.get("")
async def listar_clientes():
    return {"Clientes": lista_clientes}

@router.get("/{cliente_id}")
async def listar_cliente(cliente_id: int):
    for objeto_cliente in lista_clientes:
        if objeto_cliente.id == cliente_id:
            return {"Cliente": objeto_cliente}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"El cliente con ID {cliente_id} no existe."
    )

@router.post("")
async def crear_clientes(datos_cliente : ClienteCrear):
    id_cliente = len(lista_clientes) + 1
    nuevo_cliente_dict = datos_cliente.model_dump()
    cliente_validado = Cliente(**nuevo_cliente_dict)
    cliente_validado.id = id_cliente
    lista_clientes.append(cliente_validado)
    return cliente_validado

@router.put("/{id}") 
async def editar_cliente(id: int, datos_actualizados: ClienteEditar):
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == id:
            datos_dict = datos_actualizados.model_dump()
            cliente_validado = Cliente(**datos_dict)
            cliente_validado.id = id
            lista_clientes[i] = cliente_validado
            return cliente_validado
    raise HTTPException(status_code=400, detail=f"El cliente con ID {id} no existe.")

@router.delete("/clientes/{id}")
async def eliminar_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            lista_clientes.remove(cliente)
            return {"mensaje": "El cliente fue eliminado con exito"}
    raise HTTPException(status_code=400, detail=f"El cliente con ID {id} no existe.")
