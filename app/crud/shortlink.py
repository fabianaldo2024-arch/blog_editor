from sqlalchemy.orm import Session
from ..models.shortlink import ShortLink
from ..schemas.shortlink import ShortLinkCreate
import secrets
import string

def generate_short_code(length=6):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_shortlink(db: Session, url: str):
    # Generar código único
    code = generate_short_code()
    while db.query(ShortLink).filter(ShortLink.short_code == code).first():
        code = generate_short_code()
    
    db_shortlink = ShortLink(original_url=url, short_code=code)
    db.add(db_shortlink)
    db.commit()
    db.refresh(db_shortlink)
    return db_shortlink

def get_shortlink(db: Session, short_code: str):
    return db.query(ShortLink).filter(ShortLink.short_code == short_code).first()

def increment_clicks(db: Session, shortlink: ShortLink):
    shortlink.clicks += 1
    db.commit()
    db.refresh(shortlink)
