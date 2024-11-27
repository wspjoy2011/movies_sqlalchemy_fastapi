from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from apps.accounts.routes import router as user_router

app = FastAPI(
    title="Test project",
    description="Description of project"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    return JSONResponse(
        status_code=422,
        content={
            "field": error["loc"][-1],
            "message": error["msg"]
        },
    )

api_version_prefix = "/api/v1"
app.include_router(user_router, prefix=f"{api_version_prefix}/accounts", tags=["users"])
