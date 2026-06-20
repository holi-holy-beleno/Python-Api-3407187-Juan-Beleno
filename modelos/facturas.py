from pydantic import BaseModel, computed_field
from modelos.clientes import Cliente
from modelos.transacciones import Transaccion
from datetime import datetime

class FacturaBase(BaseModel):
    fecha : str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cliente : Cliente | None = None
    transacciones : list[Transaccion] = []

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id : int | None = None

    @computed_field
    @property
    def valor_total(self) -> float:
        factura_id_actual = getattr(self, 'id', None)
        
        if not factura_id_actual or not self.transacciones:
            return 0.0
            
        total_factura = 0.0
        for tx in self.transacciones:
            total_factura += tx.vr_unitario * tx.cantidad
            
        return total_factura