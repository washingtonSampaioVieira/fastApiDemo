import decimal

from fastapi.testclient import TestClient

from contas_a_pagar_e_receber.routers.contas_a_pagar_e_receber_router import ContaPagarReceberRequest, \
    ContaPagarReceberResponse
from main import app

client = TestClient(app)


def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get('/contas-pagar-receber')

    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'descricao': 'aluguel', 'valor': '100.5', 'tipo': 'PAGAR'}]


def test_deve_criar_conta_a_pagar_e_receber():
    nova_conta = {
        "descricao": "Curso de Python",
        "valor": 100.50,
        "tipo": "PAGAR"
    }

    nova_conta_response = nova_conta.copy()
    nova_conta_response['id'] = 2

    response = client.post('/contas-pagar-receber', json=nova_conta)
    response_json = response.json()

    assert response.status_code == 201
    assert response_json["id"] == nova_conta_response["id"]
    assert response_json["descricao"] == nova_conta_response["descricao"]
    assert response_json["tipo"] == nova_conta_response["tipo"]
