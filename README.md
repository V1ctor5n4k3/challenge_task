# 🧠 Challenge Backend API

Este proyecto es una API RESTful construida con FastAPI, SQLAlchemy async y Pydantic v2. Está diseñada para manejar posts, comentarios y usuarios, con enfoque en robustez, modularidad y buenas prácticas modernas.

## 🚀 Tecnologías

- **FastAPI** — Framework web moderno y rápido
- **SQLAlchemy async** — ORM asíncrono para PostgreSQL
- **Pydantic v2** — Validación y serialización de datos
- **Alembic** — Migraciones de base de datos
- **Uvicorn** — Servidor ASGI

## 🛠️ Instalación

git clone https://github.com/V1ctor5n4k3/challenge_backend.git
cd challenge_backend
python -m venv venv
source venv/bin/activate  # o .\venv\Scripts\activate en Windows
pip install -r --no-cache-dir requirements.txt




## 🔄 Flujo Recomendado de Uso
Registrar usuario → POST /auth/register

Iniciar sesión → POST /auth/login (guardar token)

Crear tags → POST /tags/create_tag

Crear posts → POST /posts/create_post (usando IDs de tags)

Crear comentarios → POST /comments/create_comment (usando ID de post)



## 🧠 Notas Técnicas
Todos los modelos usan from_attributes = True para compatibilidad con Pydantic v2

Se aplica borrado lógico con is_deleted = True en lugar de eliminación física

Las relaciones se cargan con selectinload para evitar errores de serialización

Autenticación basada en JWT (JSON Web Tokens)

Validación automática de datos con Pydantic v2

Manejo asíncrono de base de datos para mejor performance



## 📋 Colección Postman
Incluye un archivo Blog-API-FastAPI.postman_collection.json con todos los endpoints preconfigurados, incluyendo:

Variables de entorno para base URL y tokens

Tests automáticos para verificar respuestas

Ejemplos de requests listos para usar

Configuración de headers de autenticación



## 🚀 Ejecución
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4


## 🐳 Docker

### Construir la imagen

docker build -t challenge-backend-api .
Ejecutar el contenedor

docker run -p 8000:8000 --name challenge-api challenge-backend-api
Ejecutar en segundo plano

docker run -d -p 8000:8000 --name challenge-api challenge-backend-api
Variables de entorno
Puedes sobreescribir las variables de entorno al ejecutar el contenedor:


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




## 🧑‍💻 Autor
#Victor Felipe Lugo Gonzalez

##Especialista en backend Python, FastAPI y automatización avanzada.
