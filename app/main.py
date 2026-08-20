from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from pydantic import BaseModel, EmailStr
import secrets
from .api import shortlinks, auth, posts, users
from .database import engine, Base

from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .crud import post as post_crud

# ========== INSTANCIA DE LA APP ==========
app = FastAPI(
    title="Blog TECHSILVER",
    description="API para blog personal con autenticación JWT",
    version="1.0.0"
)

# ========== MIDDLEWARES ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="tu_clave_secreta_aqui")  # ¡Cambia por una clave real!

# ========== ARCHIVOS ESTÁTICOS ==========
# Monta la carpeta 'static' para servir CSS, JS, imágenes, etc.
# La ruta física es 'app/static', y se servirá en /static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ========== PLANTILLAS ==========
# Configura la carpeta de plantillas (dentro de 'app/templates')
templates = Jinja2Templates(directory="app/templates")

# ========== FUNCIÓN CSRF ==========
def generate_csrf_token(request):
    token = secrets.token_hex(32)
    request.session["csrf_token"] = token
    return token

# ========== MODELO PARA CONTACTO ==========
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

# ========== CREAR TABLAS ==========
Base.metadata.create_all(bind=engine)

# ========== ROUTERS ==========
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(shortlinks.router, prefix="/s", tags=["shortlinks"])

# ========== RUTAS FRONTEND ==========

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user_authenticated = request.session.get("user_id") is not None
    posts = post_crud.get_posts(db, skip=0, limit=20)
    return templates.TemplateResponse("pages/index.html", {
        "request": request,
        "user_authenticated": user_authenticated,
        "posts": posts
    })

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Blog TECHSILVER funcionando correctamente"}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("pages/register.html", {"request": request})

@app.get("/create-post", response_class=HTMLResponse)
async def create_post_page(request: Request):
    return templates.TemplateResponse("pages/create_post.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    user_authenticated = request.session.get("user_id") is not None
    return templates.TemplateResponse("pages/about.html", {
        "request": request,
        "user_authenticated": user_authenticated
    })

@app.get("/contact", response_class=HTMLResponse)
async def contact_get(request: Request):
    user_authenticated = request.session.get("user_id") is not None
    csrf_token = generate_csrf_token(request)
    return templates.TemplateResponse(
        "pages/contact.html",
        {
            "request": request,
            "user_authenticated": user_authenticated,
            "csrf_token": csrf_token
        }
    )

@app.post("/contact")
async def contact_post(
    request: Request,
    name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...),
    csrf_token: str = Form(...)
):
    # Verificar CSRF
    session_token = request.session.get("csrf_token")
    if not session_token or session_token != csrf_token:
        return RedirectResponse(url="/contact?error=csrf", status_code=403)

    # Los datos ya están validados por FastAPI (name, email, message)
    # Aquí procesas el mensaje (enviar correo, guardar en BD, etc.)
    form = ContactForm(name=name, email=email, message=message)
    # Por ahora solo redirigimos con éxito
    return RedirectResponse(url="/contact?gracias=true", status_code=303)

# ========== INICIO (para ejecutar con uvicorn) ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)