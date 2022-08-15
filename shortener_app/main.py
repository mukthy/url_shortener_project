from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import validators
from . import schemas
from .database import SessionLocal, engine
import secrets

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API"


@app.post("/url")
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        return raise_bad_request(message="The URL you have provided is not valid")
    # return f"TODO: Create database entry for {url.target_url}"
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for i in range(5))
    secret_key = "".join(secrets.choice(chars) for i in range(8))
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url
