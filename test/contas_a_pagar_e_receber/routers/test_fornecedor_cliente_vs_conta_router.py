from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.dependencies import get_db
from main import app
from app.core.config.databse import Base

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def overide_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db()] = overide_get_db


def test_deve_listar_contas_de_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/fornecedor-cliente', json={'nome': "ENEL"})

    client.post('/contas-pagar-receber',
                json={'descricao': 'aluguel', 'valor': '100.0000000000', 'tipo': 'PAGAR', 'fornecedor_client_id': 1})

    client.post('/contas-pagar-receber',
                json={'descricao': 'Conta de Luz', 'valor': '100.0000000000', 'tipo': 'PAGAR',
                      'fornecedor_client_id': 1})

    response = client.get('/fornecedor-cliente/1/contas-pagar-receber')

    assert response.status_code == 200
    assert response.json() == [
        {'data_baixa': None, 'descricao': 'aluguel', 'esta_baixada': False, 'fornecedor': {'id': 1, 'nome': 'ENEL'},
         'id': 1, 'tipo': 'PAGAR', 'valor': '100.0000000000', 'valor_da_baixa': None},

        {'data_baixa': None, 'descricao': 'Conta de Luz', 'esta_baixada': False, 'fornecedor': {'id': 1, 'nome': 'ENEL'},
         'id': 2, 'tipo': 'PAGAR', 'valor': '100.0000000000', 'valor_da_baixa': None}
    ]

    def test_deve_retornar_lista_vazia_de_fornecedor_cliente():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        response = client.get('/fornecedor-cliente/1/contas-pagar-receber')

        assert response.status_code == 200
        assert response.json() == []
