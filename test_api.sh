#!/bin/bash

BASE_URL="http://127.0.0.1:8000"
USERNAME="testuser"
PASSWORD="testpass"
EMAIL="test@example.com"

echo "=== Registrando usuario ==="
curl -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}"
echo -e "\n"

echo "=== Iniciando sesión ==="
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME&password=$PASSWORD")

TOKEN=$(echo $RESPONSE | jq -r '.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ Error al obtener el token. Respuesta del login: $RESPONSE"
  exit 1
fi
echo "✅ Token obtenido: $TOKEN"
echo -e "\n"

echo "=== Creando un post ==="
curl -X POST "$BASE_URL/posts/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Post automático desde script", "content": "Contenido generado automáticamente"}'
echo -e "\n"

echo "=== Listando todos los posts ==="
curl -X GET "$BASE_URL/posts/" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "✅ Prueba completada."
