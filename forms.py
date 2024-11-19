import os

from fastapi import FastAPI, Form, File, UploadFile

app = FastAPI()

UPLOAD_DIR = "files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/users/")
async def create_user(name: str = Form(...), age: int = Form(...), avatar: UploadFile = File(...)):
    return {
        "name": name,
        "age": age,
        "file_size": avatar.size,
        "file_name": avatar.filename,
        "file_content_type": avatar.content_type,
    }


@app.post("/upload/")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    saved_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        saved_files.append({
            "file_name": file.filename,
            "content_type": file.content_type,
            "file_path": file_path
        })

    return saved_files
