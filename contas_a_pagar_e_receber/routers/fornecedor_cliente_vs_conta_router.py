from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models.conta_a_pagar_receber_model import ContaPagarReceber
from contas_a_pagar_e_receber.routers.contas_a_pagar_e_receber_router import ContaPagarReceberResponse
from shared.dependencies import get_db

router = APIRouter(prefix="/fornecedor-cliente")


@router.get("/{id}/contas-pagar-receber", response_model=List[ContaPagarReceberResponse])
def obter_contas_a_pagar_de_um_fornecedor_cliente_por_id(id: int, db: Session = Depends(get_db)) \
        -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).filter_by(fornecedor_client_id=id)
