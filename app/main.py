from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .api import shortlinks

from .database import engine, Base
from .api import auth, posts, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog TECHSILVER",
    description="API para blog personal con autenticación JWT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar templates y archivos estáticos
templates = Jinja2Templates(directory="templates")

# --- SOLUCIÓN 1: Si quieres usar app/static, usa esta línea ---
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
# --- SOLUCIÓN 2: Si creaste la carpeta static en la raíz, usa esta ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# ========== INCLUIR ROUTERS DE LA API ==========
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(shortlinks.router, prefix="/s", tags=["shortlinks"])


# ========== RUTAS PARA EL FRONTEND ==========
@app.get("/")
async def home(request: Request):
    """Página principal del blog"""
    return templates.TemplateResponse("pages/index.html", {"request": request})

# COMENTA estas líneas si no tienes login.html, register.html o dashboard.html
# @app.get("/login")
# async def login_page(request: Request):
#     return templates.TemplateResponse("pages/login.html", {"request": request})

# @app.get("/register")
# async def register_page(request: Request):
#     return templates.TemplateResponse("pages/register.html", {"request": request})

# @app.get("/dashboard")
# async def dashboard_page(request: Request):
#     return templates.TemplateResponse("pages/dashboard.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Blog TECHSILVER funcionando correctamente"}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("pages/register.html", {"request": request})

@app.get("/create-post")
async def create_post_page(request: Request):
    return templates.TemplateResponse("pages/create_post.html", {"request": request})
