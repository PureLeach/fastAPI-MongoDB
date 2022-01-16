import uvicorn
from fastapi import FastAPI

from core import settings
from api import endpoints


app = FastAPI()
app.include_router(endpoints.router)


if __name__ == "__main__":
    """Launched with `python main.py` at root level"""
    config: dict = settings.settings["fastAPI"]
    uvicorn.run("main:app", host=config["host"], port=config["port"], reload=config["reload"])
