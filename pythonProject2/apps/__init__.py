from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status, Request


def create_app():
    app = FastAPI()

    @app.exception_handler(Exception)
    def authjwt_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.args[0]}
        )

    from apps.Users.routers import user_api_router

    app.include_router(user_api_router)
    return app
