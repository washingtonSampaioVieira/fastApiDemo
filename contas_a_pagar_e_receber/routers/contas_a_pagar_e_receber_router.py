from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List
from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models.conta_a_pagar_receber_model import ContaPagarReceber
from contas_a_pagar_e_receber.models.fornecedor_cliente_model import FornecedorCliente
from contas_a_pagar_e_receber.routers.fornecedor_cliente_router import FornecedorClienteResponse
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix='/contas-pagar-receber')


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


class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'


class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum
    fornecedor_client_id: int | None = None


@router.get('/', response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()


@router.get('/{id}', response_model=ContaPagarReceberResponse)
def listar_conta(id: int, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    conta = busca_conta_por_id(id, db)

    if conta is None:
        raise NotFound("Conta a pagar e receber")

    return conta


@router.post('/', response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta_request: ContaPagarReceberRequest, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    valida_fornecedor(conta_request.fornecedor_client_id, db)

    contas_a_pagar_e_receber = ContaPagarReceber(
        **conta_request.dict()
    )

    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)

    return contas_a_pagar_e_receber


@router.put('/{id}', response_model=ContaPagarReceberResponse, status_code=201)
def atualizar_conta(id: int, conta_request: ContaPagarReceberRequest,
                    db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    valida_fornecedor(conta_request.fornecedor_client_id, db)

    conta_pagar_receber = busca_conta_por_id(id, db)

    conta_pagar_receber.tipo = conta_request.tipo
    conta_pagar_receber.valor = conta_request.valor
    conta_pagar_receber.descricao = conta_request.descricao
    conta_pagar_receber.fornecedor_client_id = conta_request.fornecedor_client_id

    db.add(conta_pagar_receber)
    db.commit()
    db.refresh(conta_pagar_receber)

    return conta_pagar_receber


@router.post('/{id}/baixar', response_model=ContaPagarReceberResponse, status_code=201)
def baixar_conta(id: int, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    conta_pagar_receber = busca_conta_por_id(id, db)

    if conta_pagar_receber.esta_baixada and conta_pagar_receber.valor == conta_pagar_receber.valor_da_baixa:
        return conta_pagar_receber

    conta_pagar_receber.data_baixa = datetime.now()
    conta_pagar_receber.esta_baixada = True
    conta_pagar_receber.valor_da_baixa = conta_pagar_receber.valor

    db.add(conta_pagar_receber)
    db.commit()
    db.refresh(conta_pagar_receber)

    return conta_pagar_receber


@router.delete('/{id}', status_code=204)
def deletar_conta(id: int, db: Session = Depends(get_db)) -> None:
    conta_pagar_receber = busca_conta_por_id(id, db)
    db.delete(conta_pagar_receber)

    db.commit()


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
