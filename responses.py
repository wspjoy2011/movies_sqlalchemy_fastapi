from pathlib import Path

from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from starlette.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse

app = FastAPI()


class Post(BaseModel):
    title: str


posts = {
    1: Post(title="Hello"),
}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post


@app.delete("/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    posts.pop(post_id, None)
    return None


@app.put("/posts/{post_id}/")
async def update_or_create_post(post_id: int, post: Post, response: Response):
    if post_id not in posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    posts[post_id] = post
    response.status_code = status.HTTP_200_OK
    return posts[post_id]


@app.get("/html/", response_class=HTMLResponse)
async def get_html():
    return """
        <html>
            <head>
                <title>Hello world!</title>
            </head>
            <body>
                <h1>Hello world!</h1>
            </body>
        </html>
    """


@app.get("/text/", response_class=PlainTextResponse)
async def text():
    return "Hello world!"


@app.get("/redirect/")
async def redirect():
    return RedirectResponse(
        "/text/",
        status_code=status.HTTP_301_MOVED_PERMANENTLY
    )

@app.get("/download/")
async def get_cat():
    root_directory = Path(__file__).parent
    picture_path = root_directory / "assets" / "cat.jpg"
    return FileResponse(picture_path)
