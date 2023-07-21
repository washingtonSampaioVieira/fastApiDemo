from sqlalchemy.orm import Session

from app.core.model.conta_a_pagar_receber_model import ContaPagarReceber
from app.core.model.fornecedor_cliente_model import FornecedorCliente
from app.core.exception.exceptions import NotFound


def busca_conta_por_id(id: int, db: Session) -> ContaPagarReceber:
    conta_pagar_receber = db.query(ContaPagarReceber).get(id)

    if conta_pagar_receber is None:
        raise NotFound("conta a pagar e receber")

    return conta_pagar_receber


def valida_fornecedor(id, db: Session) -> None:
    if id is not None:
        fornecedor = db.query(FornecedorCliente).get(id)

        if fornecedor is None:
            raise NotFound("fornecedor cliente")
