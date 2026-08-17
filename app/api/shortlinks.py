from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from ..database import get_db
from ..crud import shortlink as crud
from ..schemas.shortlink import ShortLinkCreate, ShortLinkResponse

router = APIRouter()

@router.post("/shorten", response_model=ShortLinkResponse)
def shorten_url(link: ShortLinkCreate, db: Session = Depends(get_db)):
    return crud.create_shortlink(db, link.original_url)

@router.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    link = crud.get_shortlink(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")
    crud.increment_clicks(db, link)
    return RedirectResponse(url=link.original_url)

@router.get("/stats/{short_code}", response_model=ShortLinkResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    link = crud.get_shortlink(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")
    return link
