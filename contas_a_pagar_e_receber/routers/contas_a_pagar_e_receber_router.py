from decimal import Decimal
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/contas-pagar-receber')


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str


class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str


@router.get('/', response_model=List[ContaPagarReceberResponse])
def listar_contas():
    return [
        ContaPagarReceberResponse(
            id=1,
            descricao="aluguel",
            valor=100.50,
            tipo="PAGAR"
        )
    ]


@router.post('/', response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    return ContaPagarReceberResponse(
        id=2,
        descricao=conta.descricao,
        valor=conta.valor,
        tipo=conta.tipo
    )
