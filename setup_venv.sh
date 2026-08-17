PROJECT_DIR="blog_project"
VENV_DIR="$PROJECT_DIR/venv"

echo "======================================"
echo " Configurando entorno virtual"
echo "======================================"

# 1. Verificar que la carpeta del proyecto exista
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ No se encontró la carpeta '$PROJECT_DIR'."
    echo "   Corré este script desde el mismo lugar donde ejecutaste create_structure.py"
    exit 1
fi

# 2. Verificar que python3-venv esté disponible; si no, instalarlo
if ! python3 -c "import venv" &> /dev/null; then
    echo "⚙️  Instalando python3-venv (necesita tu contraseña de sudo)..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# 3. Crear el entorno virtual si no existe
if [ -d "$VENV_DIR" ]; then
    echo "✅ El entorno virtual ya existe en: $VENV_DIR"
else
    echo "📦 Creando entorno virtual en: $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# 4. Activar el entorno virtual
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
echo "✅ Entorno virtual activado: $(which python3)"

# 5. Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# 6. Instalar dependencias desde requirements.txt
REQ_FILE="$PROJECT_DIR/requirements.txt"
if [ -f "$REQ_FILE" ]; then
    echo "📥 Instalando dependencias desde $REQ_FILE ..."
    pip install -r "$REQ_FILE"
else
    echo "⚠️  No se encontró $REQ_FILE, se omite la instalación de dependencias."
fi

echo ""
echo "======================================"
echo " ✅ Todo listo"
echo "======================================"
echo "El entorno virtual quedó activado en esta terminal."
echo ""
echo "La próxima vez que abras una terminal nueva, activalo con:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "Para desactivarlo en cualquier momento:"
echo "  deactivate"