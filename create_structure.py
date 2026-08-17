#!/usr/bin/env python3
"""
create_structure.py

Crea automáticamente el árbol de carpetas y archivos vacíos
para el proyecto blog_project (FastAPI + SQLAlchemy + Alembic).

Uso:
    python3 create_structure.py

Se puede ejecutar varias veces sin peligro: si una carpeta o
archivo ya existe, simplemente se omite (no se sobrescribe nada).
"""

import os

# Carpeta raíz del proyecto (se crea en el directorio actual)
ROOT = "blog_project"

# Lista de carpetas a crear (rutas relativas a ROOT)
DIRECTORIES = [
    "app",
    "app/models",
    "app/schemas",
    "app/crud",
    "app/api",
    "app/api/v1",
    "app/api/v1/endpoints",
    "app/core",
    "app/templates",
    "app/templates/auth",
    "app/templates/articles",
    "app/templates/comments",
    "app/templates/admin",
    "app/templates/includes",
    "app/static",
    "app/static/css",
    "app/static/js",
    "app/static/images",
    "app/utils",
    "app/migrations",
    "tests",
]

# Lista de archivos a crear (rutas relativas a ROOT).
# Los archivos vacíos de este listado quedarán con 0 bytes,
# listos para que empieces a escribir el código.
FILES = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/database.py",

    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/article.py",
    "app/models/tag.py",
    "app/models/comment.py",

    "app/schemas/__init__.py",
    "app/schemas/user.py",
    "app/schemas/article.py",
    "app/schemas/tag.py",
    "app/schemas/comment.py",

    "app/crud/__init__.py",
    "app/crud/user.py",
    "app/crud/article.py",
    "app/crud/tag.py",
    "app/crud/comment.py",

    "app/api/__init__.py",
    "app/api/v1/__init__.py",
    "app/api/v1/router.py",
    "app/api/v1/endpoints/__init__.py",
    "app/api/v1/endpoints/auth.py",
    "app/api/v1/endpoints/users.py",
    "app/api/v1/endpoints/articles.py",
    "app/api/v1/endpoints/comments.py",
    "app/api/v1/endpoints/tags.py",

    "app/core/__init__.py",
    "app/core/security.py",
    "app/core/dependencies.py",
    "app/core/exceptions.py",

    "app/templates/base.html",

    "app/utils/__init__.py",
    "app/utils/markdown.py",
    "app/utils/sanitizer.py",
    "app/utils/search.py",
    "app/utils/pagination.py",

    ".env",
    "requirements.txt",
    "docker-compose.yml",
    "Dockerfile",
    "README.md",
]

# Archivos con un poco de contenido inicial (opcional, útil como base)
INITIAL_CONTENT = {
    "README.md": "# Blog Project\n\nProyecto de blog construido con FastAPI.\n",
    "requirements.txt": (
        "fastapi\n"
        "uvicorn[standard]\n"
        "sqlalchemy\n"
        "alembic\n"
        "pydantic\n"
        "python-dotenv\n"
        "passlib[bcrypt]\n"
        "python-jose\n"
    ),
    ".env": "DATABASE_URL=postgresql://user:password@localhost:5432/blog_db\nSECRET_KEY=change_this_secret\n",
}


def create_directories(root: str, dirs: list) -> None:
    for d in dirs:
        path = os.path.join(root, d)
        os.makedirs(path, exist_ok=True)
        print(f"[DIR ]  {path}")


def create_files(root: str, files: list, initial_content: dict) -> None:
    for f in files:
        path = os.path.join(root, f)
        # Asegura que la carpeta contenedora exista (por si acaso)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if os.path.exists(path):
            print(f"[SKIP]  {path} (ya existe)")
            continue

        content = initial_content.get(f, "")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"[FILE]  {path}")


def main() -> None:
    print(f"Creando estructura del proyecto en: ./{ROOT}\n")
    create_directories(ROOT, DIRECTORIES)
    create_files(ROOT, FILES, INITIAL_CONTENT)
    print("\n✅ Estructura creada correctamente.")
    print(f"Entra al proyecto con:  cd {ROOT}")


if __name__ == "__main__":
    main()