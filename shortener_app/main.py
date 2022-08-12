from fastapi import FastAPI, HTTPException
import validators
from . import schemas

app = FastAPI()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API"


@app.post("/url")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        return raise_bad_request(message="The URL you have provided is not valid")
    return f"TODO: Create database entry for {url.target_url}"
