# Editor de Blog

Aplicación web para gestión de blogs con autenticación, operaciones CRUD y vistas con plantillas HTML. Construida con Python y un framework moderno (FastAPI o Flask).

## 🚀 Tecnologías utilizadas
- **Backend:** Python (FastAPI / Flask)
- **Base de datos:** SQLite (`blog.db`)
- **ORM:** SQLAlchemy
- **Validación:** Pydantic (schemas)
- **Frontend:** HTML + Jinja2 (plantillas)
- **Contenerización:** Docker y Docker Compose

## 📁 Estructura del proyecto

Blog_Editor/
├── app/ # Código principal
│ ├── api/ # Rutas de la API
│ ├── auth/ # Lógica de autenticación
│ ├── crud/ # Operaciones con la BD
│ ├── models/ # Modelos de SQLAlchemy
│ ├── schemas/ # Esquemas de Pydantic
│ ├── static/ # Archivos estáticos (CSS, JS)
│ ├── database.py # Configuración de la BD
│ └── main.py # Punto de entrada
├── templates/ # Plantillas Jinja2
│ ├── base/ # Plantilla base
│ └── pages/ # Páginas específicas
│ ├── create_post.html
│ ├── index.html
│ ├── login.html
│ └── register.html
├── static/ # Archivos estáticos globales
├── requirements.txt # Dependencias de Python
├── Dockerfile # Instrucciones para Docker
├── docker-compose.yml # Orquestación con Docker
├── create_structure.py # Utilidad de creación
├── setup_app.sh # Script de configuración
├── setup_venv.sh # Script del entorno virtual
└── test_api.sh # Script de pruebas de API
