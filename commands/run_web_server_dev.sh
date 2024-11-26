#!/bin/sh

# Run web server
uvicorn /usr/src/fastapi/main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /usr/src/fastapi/
