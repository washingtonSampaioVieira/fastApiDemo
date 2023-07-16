from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from shared.databse import Base
from shared.dependencies import get_db

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


def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/contas-pagar-receber', json={'descricao': 'aluguel', 'valor': '100.0000000000', 'tipo': 'PAGAR'})
    client.post('/contas-pagar-receber', json={'descricao': 'aluguel', 'valor': '100.0000000000', 'tipo': 'PAGAR'})

    response = client.get('/contas-pagar-receber')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'descricao': 'aluguel', 'valor': '100.0000000000', 'tipo': 'PAGAR'},
        {'id': 2, 'descricao': 'aluguel', 'valor': '100.0000000000', 'tipo': 'PAGAR'}
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    nova_conta = {
        "descricao": "Curso de Python",
        "valor": 100.50,
        "tipo": "PAGAR"
    }

    nova_conta_response = nova_conta.copy()
    nova_conta_response['id'] = 1

    response = client.post('/contas-pagar-receber', json=nova_conta)
    response_json = response.json()

    assert response.status_code == 201
    assert response_json["id"] == nova_conta_response["id"]
    assert response_json["descricao"] == nova_conta_response["descricao"]
    assert response_json["tipo"] == nova_conta_response["tipo"]


def test_deve_listar_por_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    nova_conta = {
        "descricao": "Curso de Python",
        "valor": 100.50,
        "tipo": "PAGAR"
    }

    nova_conta_response = nova_conta.copy()
    nova_conta_response['id'] = 1

    response = client.post('/contas-pagar-receber', json=nova_conta)
    response_get = client.get(f'/contas-pagar-receber/{response.json()["id"]}')
    response_json = response_get.json()

    assert response_get.status_code == 200
    assert response_json["id"] == nova_conta_response["id"]
    assert response_json["descricao"] == nova_conta_response["descricao"]
    assert response_json["tipo"] == nova_conta_response["tipo"]


def test_deve_retornar_nao_encontrado():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.get('/contas-pagar-receber/1')
    response_json = response_get.json()

    assert response_get.status_code == 404
    assert response_json["message"] == "Oops! conta a pagar e receber não encontrado"


def test_deve_retornar_erro_quando_exceder_a_descricao():
    response = client.post('/contas-pagar-receber', json={
        'descricao': '123456789012345678123412901234567890',
        'valor': '100',
        'tipo': 'PAGAR'
    })

    assert response.status_code == 422


def test_deve_retornar_erro_quando_a_descricao_for_menor_que_3():
    response = client.post('/contas-pagar-receber', json={
        'descricao': '12',
        'valor': '100',
        'tipo': 'PAGAR'
    })

    assert response.status_code == 422


def test_deve_retornar_erro_quando_o_tipo_for_invalido():
    response = client.post('/contas-pagar-receber', json={
        'descricao': '1223',
        'valor': '100',
        'tipo': 'FIADO'
    })

    assert response.status_code == 422
    assert response.json()['detail'][0]['ctx'] == {"expected": "'PAGAR' or 'RECEBER'"}


def test_deve_retornar_erro_quando_valor_for_zero_ou_menor():
    response = client.post('/contas-pagar-receber', json={
        'descricao': 'Descrição',
        'valor': -1,
        'tipo': 'PAGAR'
    })
    assert response.status_code == 422

    response = client.post('/contas-pagar-receber', json={
        'descricao': 'Descrição',
        'valor': 0,
        'tipo': 'PAGAR'
    })

    assert response.status_code == 422


def test_deve_atualizar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/contas-pagar-receber',
                           json={'descricao': 'aluguel', 'valor': '100.0000000000', 'tipo': 'PAGAR'})

    id_contas_pagar_receber = response.json()['id']

    response_put = client.put(f'/contas-pagar-receber/{id_contas_pagar_receber}', json={
        'descricao': 'Descrição atualizada',
        'valor': '110',
        'tipo': 'PAGAR'
    })

    assert response_put.status_code == 201
    assert response_put.json()['descricao'] == 'Descrição atualizada'


def test_deve_deletar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/contas-pagar-receber',
                           json={'descricao': 'aluguel', 'valor': '100.0000000000', 'tipo': 'PAGAR'})

    id_contas_pagar_receber = response.json()['id']

    response_put = client.delete(f'/contas-pagar-receber/{id_contas_pagar_receber}')
    response_get = client.get(f'/contas-pagar-receber')

    assert response_put.status_code == 204
    assert response_get.json() == []


