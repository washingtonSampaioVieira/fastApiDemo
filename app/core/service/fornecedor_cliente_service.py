from sqlalchemy.orm import Session

from app.core.model.fornecedor_cliente_model import FornecedorCliente
from app.core.router.response.fornecedor_cliente_response import FornecedorClienteResponse
from app.core.exception.exceptions import NotFound


def buscar_fornecedor_cliente_por_id(id, db: Session) -> FornecedorClienteResponse:
    fornecedor_cliente = db.query(FornecedorCliente).get(id)

    if fornecedor_cliente is None:
        raise NotFound("fornecedor Cliente")

    return fornecedor_cliente
