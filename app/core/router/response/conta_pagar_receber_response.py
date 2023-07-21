from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.core.router.response.fornecedor_cliente_response import FornecedorClienteResponse


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str
    fornecedor: FornecedorClienteResponse | None = None
    data_baixa: datetime | None = None
    valor_da_baixa: Decimal | None = None
    esta_baixada: bool | None = None

    class Config:
        orm_mode = True
