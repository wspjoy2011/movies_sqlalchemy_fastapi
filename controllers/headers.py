from fastapi import FastAPI, Header, Cookie
from starlette.responses import JSONResponse, Response

app = FastAPI()

@app.get("/")
async def get_header(hello: str = Header(...)):
    return {"hello": hello}


# @app.get("/user-agent/")
# async def get_header(user_agent: str = Header(...)):
#     return {"user_agent": user_agent}


@app.get("/user-agent/")
async def get_header(user_agent: str = Header(...)):
    custom_header = {"X-Custom-Header": "MyCustomValue"}

    return JSONResponse(
        content={"user_agent": user_agent},
        headers=custom_header
    )


@app.get("/cookie/")
async def get_cookie(hello: str | None = Cookie(None)):
    return {"hello": hello}


@app.get("/set-cookie/")
async def set_cookie(response: Response):
    response.set_cookie(key="hello", value="world!!!", httponly=True)
    return {"message": "Cookie has been set"}
