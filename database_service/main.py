import uvicorn
from fastapi import FastAPI

from api import endpoints
from core.settings import SERVER_HOST, SERVER_PORT, SERVER_RELOAD

app = FastAPI()
app.include_router(endpoints.router)


if __name__ == '__main__':
    """Launched with `python main.py` at root level"""
    uvicorn.run('main:app', host=SERVER_HOST, port=SERVER_PORT, reload=SERVER_RELOAD)
