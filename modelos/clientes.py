from pydantic import BaseModel

class Cliente(BaseModel):
    id : int
    nombre : str
    descripcion : str | None = None

class ClienteBase(BaseModel):
    nombre : str
    descripcion : str | None = None

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase):
    id : int | None = None