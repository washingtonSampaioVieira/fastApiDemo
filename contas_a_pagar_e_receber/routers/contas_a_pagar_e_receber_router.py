from decimal import Decimal
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/contas-a-pagar-e-receber')


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
    conta.id = 2
    return conta
