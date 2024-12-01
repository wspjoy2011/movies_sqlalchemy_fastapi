from io import BytesIO

from PIL import Image
from fastapi import UploadFile


def validate_image(avatar: UploadFile) -> None:
    supported_image_formats = ["JPG", "JPEG", "PNG"]
    max_file_size = 1 * 1024 * 1024

    contents = avatar.file.read()
    if len(contents) > max_file_size:
        raise ValueError("Image size exceeds 1 MB")

    try:
        image = Image.open(BytesIO(contents))
        avatar.file.seek(0)
        image_format = image.format
        if image_format not in supported_image_formats:
            raise ValueError(f"Unsupported image format: {image_format}. Use one of next: {supported_image_formats}")
    except IOError:
        raise ValueError("Invalid image format")
