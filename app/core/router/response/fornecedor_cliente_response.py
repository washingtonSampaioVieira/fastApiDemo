from pydantic import BaseModel


class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True
