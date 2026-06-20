from fastapi import FastAPI

from enrutadores import clientes, facturas, transacciones 

app = FastAPI(
    title="👀Sistema de Facturación Modular👀",
    description="Aprendiendo a usar el APIRouter"
)

# Registramos los enrutadores en la aplicación principal
app.include_router(clientes.router)
app.include_router(facturas.router)
app.include_router(transacciones.router)

@app.get("/")
async def inicio():
    return {"mensaje": "👀Bienvenido a la API de Facturación👀"}