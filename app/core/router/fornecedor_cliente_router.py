from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.model.conta_a_pagar_receber_model import ContaPagarReceber
from app.core.model.fornecedor_cliente_model import FornecedorCliente
from app.core.router.request.fornecedor_cliente_request import FornecedorClienteRequest
from app.core.router.response.conta_pagar_receber_response import ContaPagarReceberResponse
from app.core.router.response.fornecedor_cliente_response import FornecedorClienteResponse
from app.core.service.fornecedor_cliente_service import buscar_fornecedor_cliente_por_id
from app.core.config.dependencies import get_db

router = APIRouter(prefix="/fornecedor-cliente")


@router.get("", response_model=List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db: Session = Depends(get_db)) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).all()


@router.get("/{id}", response_model=FornecedorClienteResponse)
def obter_fornecedor_cliente_por_id(id: int, db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    return buscar_fornecedor_cliente_por_id(id, db)


@router.post("", response_model=FornecedorClienteResponse, status_code=201)
def criar_fornecedor_cliente(fornecedor_cliente_request: FornecedorClienteRequest,
                             db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor_cliente = FornecedorCliente(
        **fornecedor_cliente_request.dict()
    )

    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)

    return fornecedor_cliente


@router.put("/{id}", response_model=FornecedorClienteResponse, status_code=201)
def atualiza_fornecedor_cliente(id: int, fornecedor_cliente_request: FornecedorClienteRequest,
                                db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor_cliente = buscar_fornecedor_cliente_por_id(id, db)
    fornecedor_cliente.nome = fornecedor_cliente_request.nome

    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)

    return fornecedor_cliente


@router.delete("/{id}", status_code=204)
def excluir_fornecedor_cliente(id: int, db: Session = Depends(get_db)) -> None:
    fornecedor_cliente = buscar_fornecedor_cliente_por_id(id, db)

    db.delete(fornecedor_cliente)
    db.commit()


@router.get("/{id}/contas-pagar-receber", response_model=List[ContaPagarReceberResponse])
def obter_contas_a_pagar_de_um_fornecedor_cliente_por_id(id: int, db: Session = Depends(get_db)) \
        -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).filter_by(fornecedor_client_id=id)
