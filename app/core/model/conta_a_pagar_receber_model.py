from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.core.config.databse import Base


class ContaPagarReceber(Base):
    __tablename__ = 'app'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30))
    data_baixa = Column(DateTime())
    valor_da_baixa = Column(Numeric)
    esta_baixada = Column(Boolean, default=False)

    fornecedor_client_id = Column(Integer, ForeignKey("fornecedor_cliente.id"), nullable=True)
    fornecedor = relationship("FornecedorCliente")
