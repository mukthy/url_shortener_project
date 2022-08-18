from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import validators
from . import schemas, models, crud
from .database import SessionLocal, engine


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f"URL {request.url} not found"
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API"


@app.post("/url")
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        return raise_bad_request(message="The URL you have provided is not valid")
    # return f"TODO: Create database entry for {url.target_url}"
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


@app.get("/{url_key}")
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = (db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first())

    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)