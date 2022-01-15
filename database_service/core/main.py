import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def index():
    return "Hello world"


if __name__ == '__main__':
    """Launched with `python main.py` at root level"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)