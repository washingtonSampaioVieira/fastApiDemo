from pydantic import BaseModel, Field


class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=255)
