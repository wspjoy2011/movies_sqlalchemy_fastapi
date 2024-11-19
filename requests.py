from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()


@app.get("/")
async def get_request_object(request: Request):
    return {"path": request.url.path}
