# fastApiDemo
Aplicação feita com FastApi para estudar ferramenta


## Subir banco com Docker:

`docker run --name db_fast_api -p 5432:5432 -e POSTGRES_DB=db_fast_api -e POSTGRES_PASSWORD=1234 -d postgres`

## Como rodar a aplicação
`pip install requirements.txt` 

`alembic upgrade head` para criar as tabelas no banco


Após isso é só rodar a main.py na sua IDE


## Dicas
[Guide API REST](https://github.com/NationalBankBelgium/REST-API-Design-Guide/wiki/CRUD-Delete-Single-item)
