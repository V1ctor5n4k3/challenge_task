# 🧠 Challenge Backend API

Este proyecto es una API RESTful construida con FastAPI, SQLAlchemy async y Pydantic v2. Está diseñada para manejar posts, comentarios y usuarios, con enfoque en robustez, modularidad y buenas prácticas modernas.

## 🚀 Tecnologías

- **FastAPI** — Framework web moderno y rápido
- **SQLAlchemy async** — ORM asíncrono para PostgreSQL
- **Pydantic v2** — Validación y serialización de datos
- **Alembic** — Migraciones de base de datos
- **Uvicorn** — Servidor ASGI

## 📦 Estructura del proyecto
.
├── routers/ # Endpoints organizados por recurso
├── models/ # Modelos SQLAlchemy
├── schemas/ # Esquemas Pydantic v2
├── core/ # Configuración, dependencias, permisos
├── db/ # Conexión y base declarativa
├── middleware/ # Middleware personalizado
└── main.py # Punto de entrada

text

## 🛠️ Instalación

```bash
git clone https://github.com/V1ctor5n4k3/challenge_backend.git
cd challenge_backend
python -m venv venv
source venv/bin/activate  # o .\venv\Scripts\activate en Windows
pip install -r --no-cache-dir requirements.txt


📮 Endpoints de la API
🔐 Autenticación
POST /auth/register
Crea un nuevo usuario en el sistema.

Body:

json
{
  "email": "usuario@ejemplo.com",
  "password": "password123",
  "full_name": "Juan Pérez"
}
Respuesta:

json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}


POST /auth/login
Inicia sesión y obtiene token de acceso.

Body:

json
{
  "email": "usuario@ejemplo.com",
  "password": "password123"
}
Respuesta:

json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
👤 Usuarios
GET /users/me
Obtiene el perfil del usuario autenticado.

Headers:
Authorization: Bearer <token>
Respuesta:

json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "full_name": "Juan Pérez",
  "is_active": true
}
GET /users/list_users
Lista todos los usuarios (no eliminados) del sistema.

Headers:
Authorization: Bearer <token>
Parámetros Query:

skip: Número de registros a saltar (default: 0)

limit: Límite de resultados (default: 10, max: 100)

📝 Posts
POST /posts/create_post
Crea un nuevo post.

Headers:
Authorization: Bearer <token>
Content-Type: application/json
Body:

json
{
  "title": "Mi primer post",
  "content": "Este es el contenido de mi primer post...",
  "tags_ids": [1, 2]
}



GET /posts/all_post
Obtiene todos los posts del usuario autenticado.

Headers:
Authorization: Bearer <token>
Parámetros Query:

skip: Número de registros a saltar (default: 0)

limit: Límite de resultados (default: 100, max: 100)


PUT /posts/{post_id}
Actualiza un post existente.

Headers:
Authorization: Bearer <token>
Content-Type: application/json
Body:

json
{
  "title": "Post actualizado",
  "content": "Contenido actualizado del post...",
  "tags_ids": [1, 3]
}


DELETE /posts/{post_id}
Elimina lógicamente un post (soft delete).

Headers:
Authorization: Bearer <token>


💬 Comentarios
POST /comments/create_comment
Crea un nuevo comentario en un post.

Headers:
Authorization: Bearer <token>
Content-Type: application/json
Body:

json
{
  "content": "Este es un comentario interesante",
  "post_id": 1
}


GET /comments/list_comments
Lista todos los comentarios no eliminados.

Headers:
Authorization: Bearer <token>
Parámetros Query:

skip: Número de registros a saltar (default: 0)

limit: Límite de resultados (default: 10, max: 100)


🏷️ Tags
POST /tags/create_tag
Crea una nueva etiqueta.

Headers:
Authorization: Bearer <token>
Content-Type: application/json
Body:

json
{
  "name": "Tecnología",
  "description": "Posts relacionados con tecnología"
}


GET /tags/list_tags
Lista todas las etiquetas no eliminadas.

Headers:
Authorization: Bearer <token>
Parámetros Query:

skip: Número de registros a saltar (default: 0)

limit: Límite de resultados (default: 10, max: 100)

🔄 Flujo Recomendado de Uso
Registrar usuario → POST /auth/register

Iniciar sesión → POST /auth/login (guardar token)

Crear tags → POST /tags/create_tag

Crear posts → POST /posts/create_post (usando IDs de tags)

Crear comentarios → POST /comments/create_comment (usando ID de post)

🧠 Notas Técnicas
Todos los modelos usan from_attributes = True para compatibilidad con Pydantic v2

Se aplica borrado lógico con is_deleted = True en lugar de eliminación física

Las relaciones se cargan con selectinload para evitar errores de serialización

Autenticación basada en JWT (JSON Web Tokens)

Validación automática de datos con Pydantic v2

Manejo asíncrono de base de datos para mejor performance

📋 Colección Postman
Incluye un archivo Blog-API-FastAPI.postman_collection.json con todos los endpoints preconfigurados, incluyendo:

Variables de entorno para base URL y tokens

Tests automáticos para verificar respuestas

Ejemplos de requests listos para usar

Configuración de headers de autenticación

🚀 Ejecución
bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4


## 🐳 Docker

### Construir la imagen
```bash
docker build -t challenge-backend-api .
Ejecutar el contenedor
bash
docker run -p 8000:8000 --name challenge-api challenge-backend-api
Ejecutar en segundo plano
bash
docker run -d -p 8000:8000 --name challenge-api challenge-backend-api
Variables de entorno
Puedes sobreescribir las variables de entorno al ejecutar el contenedor:

bash
docker run -d -p 8000:8000 \
  -e DATABASE_URL="postgresql://usuario:password@host:5432/db" \
  -e SECRET_KEY="tu_clave_secreta" \
  --name challenge-api challenge-backend-api
Docker Compose (Recomendado)
Crea un archivo docker-compose.yml:

yaml
version: '3.9'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/challenge_db
      - SECRET_KEY=tu_clave_secreta_aqui
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=challenge_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
Ejecutar con Docker Compose:

bash
docker-compose up -d
Comandos útiles
bash
# Ver logs del contenedor
docker logs challenge-api

# Detener contenedor
docker stop challenge-api

# Eliminar contenedor
docker rm challenge-api

# Acceder al shell del contenedor
docker exec -it challenge-api bash
Notas importantes
La aplicación corre en el puerto 8000 dentro del contenedor

Asegúrate de que tu base de datos PostgreSQL esté accesible

Para desarrollo, usa --reload en el comando CMD del Dockerfile

Las variables de entorno pueden configurarse en el archivo .env o al ejecutar el contenedor

🧑‍💻 Autor
Victor Felipe Lugo Gonzalez

Especialista en backend Python, FastAPI y automatización avanzada.