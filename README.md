# Challenge Backend API

Este proyecto es una API RESTful construida con FastAPI, SQLAlchemy async y Pydantic v2. Está diseñada para manejar posts, comentarios y usuarios, con enfoque en robustez, modularidad y buenas prácticas modernas.

## Tecnologías

- **FastAPI**
- **SQLAlchemy async** 
- **Pydantic v2** 
- **Alembic** 
- **Uvicorn** 

## Instalación
```bash
git clone https://github.com/V1ctor5n4k3/challenge_backend.git

cd challenge_backend

python -m venv venv

source venv/bin/activate  

#o .\venv\Scripts\activate en Windows

pip install -r --no-cache-dir requirements.txt
```

## Migración de la Base de Datos(PostgreSQL) con Alembic

1. Modificar la cadena de conexión a la base de datos en "alembic.ini"

```bash
sqlalchemy.url = postgresql+psycopg2://postgres:postgres@localhost:5432/test
```

2. Ejecutar la migración

```bash
alembic revision --autogenerate -m "Migración inicial"

alembic upgrade head

```


## Flujo Recomendado de Uso
Registrar usuario → POST /auth/register

Iniciar sesión → POST /auth/login (guardar token)

Crear tags → POST /tags/create_tag

Crear posts → POST /posts/create_post (usando IDs de tags)

Crear comentarios → POST /comments/create_comment (usando ID de post)



## Notas Técnicas
Todos los esquemas usan from_attributes = True para compatibilidad con Pydantic v2

Se aplica borrado lógico con is_deleted = True en lugar de eliminación física

Las relaciones se cargan con selectinload para evitar errores de serialización

Autenticación basada en JWT (JSON Web Tokens)

Validación automática de datos con Pydantic v2

Manejo asíncrono de base de datos para mejor performance



## Colección Postman
Incluye un archivo challenge_backend.collection con todos los endpoints preconfigurados, incluyendo:

Variables de entorno para base URL y tokens

Ejemplos de requests listos para usar

Configuración de headers de autenticación



## Ejecución
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```


## Docker

### Construir la imagen
```bash
docker build -t challenge-backend-api .
```

Ejecutar el contenedor
```bash
docker run -p 8000:8000 --name challenge-api challenge-backend-api
```

Ejecutar en segundo plano
```bash
docker run -d -p 8000:8000 --name challenge-api challenge-backend-api
```

También puede construir la imagen y utilizar el fichero docker-compose.yml para desplegar la solución

