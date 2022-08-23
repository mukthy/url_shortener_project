from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import validators
from . import schemas, models, crud
from .database import SessionLocal, engine
from starlette.datastructures import URL
from .config import get_settings


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


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "Administration Info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.post("/url")
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        return raise_bad_request(message="The URL you have provided is not valid")
    # return f"TODO: Create database entry for {url.target_url}"
    db_url = crud.create_db_url(db=db, url=url)
    
    return get_admin_info(db_url)


@app.get("/{url_key}")
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    

    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@app.get("/admin/{secret_key}", name="Administration Info", response_model=schemas.URLInfo,)
def get_url_info(
        secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)