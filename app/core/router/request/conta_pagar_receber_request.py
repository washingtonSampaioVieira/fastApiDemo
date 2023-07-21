from decimal import Decimal

from pydantic import BaseModel, Field

from app.core.model.enum.conta_pagar_receber_tipo_enum import ContaPagarReceberTipoEnum


class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum
    fornecedor_client_id: int | None = None
