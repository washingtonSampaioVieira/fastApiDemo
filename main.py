import uvicorn
from fastapi import FastAPI

from app.core.router import fornecedor_cliente_router
from app.core.router import contas_a_pagar_e_receber_router
from app.core.exception.exceptions import NotFound
from app.core.exception.exceptions_handler import not_found_exception_handler

app = FastAPI()

app.include_router(contas_a_pagar_e_receber_router.router)
app.include_router(fornecedor_cliente_router.router)

app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
