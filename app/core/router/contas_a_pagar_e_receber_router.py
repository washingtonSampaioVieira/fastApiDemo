from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.model.conta_a_pagar_receber_model import ContaPagarReceber
from app.core.router.request.conta_pagar_receber_request import ContaPagarReceberRequest
from app.core.router.response.conta_pagar_receber_response import ContaPagarReceberResponse
from app.core.service.contas_a_pagar_e_receber_service import busca_conta_por_id, valida_fornecedor
from app.core.config.dependencies import get_db
from app.core.exception.exceptions import NotFound

router = APIRouter(prefix='/contas-pagar-receber')


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
