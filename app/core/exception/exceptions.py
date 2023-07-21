class NotFound(Exception):
    def __init__(self, name: str):
        self.name = name

# @app.exception_handlers(NotFound)
# async def unicorn_exception_handler(request: Request, exc: NotFound):
#     return JSONResponse(
#         status_code=404,
#         content={"message": f"Oops! {exc.name} não encontrado"}
#     )
