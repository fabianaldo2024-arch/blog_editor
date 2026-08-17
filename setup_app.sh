#!/bin/bash

echo "Creando estructura de archivos para Blog Editor..."

# Crear main.py
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import auth, posts, users

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="API para Blog Editor",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Blog API running"}

@app.get("/health")
def health():
    return {"status": "OK"}
EOF

# Crear database.py
cat > app/database.py << 'EOF'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF

# Crear modelos
mkdir -p app/models
cat > app/models/__init__.py << 'EOF'
from app.models.user import User
from app.models.post import Post
EOF

cat > app/models/user.py << 'EOF'
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > app/models/post.py << 'EOF'
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    author = relationship("User")
EOF

# Crear schemas
mkdir -p app/schemas
cat > app/schemas/__init__.py << 'EOF'
from app.schemas.user import UserCreate, UserResponse
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.schemas.token import Token, TokenData
EOF

cat > app/schemas/user.py << 'EOF'
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
EOF

cat > app/schemas/post.py << 'EOF'
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
EOF

cat > app/schemas/token.py << 'EOF'
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
EOF

# Crear CRUD
mkdir -p app/crud
cat > app/crud/__init__.py << 'EOF'
from app.crud import user, post
EOF

cat > app/crud/user.py << 'EOF'
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.auth import hashing

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = hashing.get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not hashing.verify_password(password, user.hashed_password):
        return False
    return user
EOF

cat > app/crud/post.py << 'EOF'
from sqlalchemy.orm import Session
from app.models import Post
from app.schemas import PostCreate, PostUpdate

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def create_post(db: Session, post: PostCreate, author_id: int):
    db_post = Post(
        title=post.title,
        content=post.content,
        published=post.published,
        author_id=author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: PostUpdate):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
EOF

# Crear API
mkdir -p app/api
cat > app/api/__init__.py << 'EOF'
from app.api import auth, posts, users
EOF

cat > app/api/auth.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, Token
from app.crud import user as user_crud
from app.auth import hashing, jwt

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    new_user = user_crud.create_user(db, user)
    return {"message": "User created successfully", "user_id": new_user.id}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
EOF

cat > app/api/posts.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import PostCreate, PostResponse, PostUpdate
from app.crud import post as post_crud
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return post_crud.get_posts(db, skip=skip, limit=limit)

@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return post_crud.create_post(db, post, current_user.id)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return post_crud.update_post(db, post_id, post_update)

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    post_crud.delete_post(db, post_id)
    return {"message": "Post deleted"}
EOF

cat > app/api/users.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import UserResponse
from app.crud import user as user_crud
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return user_crud.get_users(db, skip=skip, limit=limit)
EOF

# Actualizar auth/dependencies.py
cat > app/auth/dependencies.py << 'EOF'
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import jwt
from app.crud import user as user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = jwt.verify_token(token, credentials_exception)
    user = user_crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
EOF

echo "✅ ¡Estructura creada correctamente!"
echo "Ahora ejecuta: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
