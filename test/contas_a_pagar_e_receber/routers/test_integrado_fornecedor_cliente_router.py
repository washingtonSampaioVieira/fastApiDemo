from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.core.config.databse import Base
from app.core.config.dependencies import get_db

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


app.dependency_overrides[get_db] = overide_get_db


def test_deve_listar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/fornecedor-cliente', json={'nome': "ENEL"})
    client.post('/fornecedor-cliente', json={'nome': "Serasa"})

    response = client.get('/fornecedor-cliente')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'nome': 'ENEL'},
        {'id': 2, 'nome': 'Serasa'}
    ]


def test_deve_listar_por_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    fornecedor = {
        "nome": "ENEL",
    }

    nova_conta_response = fornecedor.copy()

    nova_conta_response['id'] = 1

    response = client.post('/fornecedor-cliente', json=fornecedor)
    response_get = client.get(f'/fornecedor-cliente/{response.json()["id"]}')
    response_json = response_get.json()

    assert response_get.status_code == 200
    assert response_json["nome"] == nova_conta_response["nome"]


def test_deve_retornar_nao_encontrado():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.get('/fornecedor-cliente/1')
    response_json = response_get.json()

    assert response_get.status_code == 404
    assert response_json["message"] == "Oops! fornecedor Cliente não encontrado"


def test_deve_criar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    fornecedor_cliente = {
        "nome": "ENEL",
    }

    nova_fornecedor_cliente = fornecedor_cliente.copy()
    nova_fornecedor_cliente['id'] = 1

    response = client.post('/fornecedor-cliente', json=fornecedor_cliente)
    response_json = response.json()

    assert response.status_code == 201
    assert response_json["nome"] == nova_fornecedor_cliente["nome"]
    assert response_json["id"] == nova_fornecedor_cliente["id"]


def test_deve_atualizar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/fornecedor-cliente', json={'nome': 'Extra'})
    id_contas_pagar_receber = response.json()['id']

    response_put = client.put(f'/fornecedor-cliente/{id_contas_pagar_receber}', json={'nome': 'Mercado DIA'})

    assert response_put.status_code == 201
    assert response_put.json()['nome'] == "Mercado DIA"
    assert response_put.json()['id'] == 1


def test_deve_deletar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/fornecedor-cliente', json={'nome': 'Extra'})
    id_contas_pagar_receber = response.json()['id']

    response_delete = client.delete(f'/fornecedor-cliente/{id_contas_pagar_receber}')

    response_get_all = client.get(f'/fornecedor-cliente')

    assert response_delete.status_code == 204
    assert response_get_all.status_code == 200
    assert response_get_all.json() == []
