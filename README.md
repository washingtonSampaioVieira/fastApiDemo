# fastApiDemo
Aplicação feita com FastApi para estudar ferramenta

## Como rodar a aplicação
`pip install requirements.txt`
Após isso é só rodar a main.py na sua IDE

## Como subir banco:

`docker run --name db_fast_api -p 5432:5432 -e POSTGRES_DB=db_fast_api -e POSTGRES_PASSWORD=1234 -d postgres`
