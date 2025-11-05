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



## Flujo Recomendado de Uso
Registrar usuario → POST /auth/register

Iniciar sesión → POST /auth/login (guardar token)

Crear tags → POST /tags/create_tag

Crear posts → POST /posts/create_post (usando IDs de tags)

Crear comentarios → POST /comments/create_comment (usando ID de post)



## Notas Técnicas
Todos los modelos usan from_attributes = True para compatibilidad con Pydantic v2

Se aplica borrado lógico con is_deleted = True en lugar de eliminación física

Las relaciones se cargan con selectinload para evitar errores de serialización

Autenticación basada en JWT (JSON Web Tokens)

Validación automática de datos con Pydantic v2

Manejo asíncrono de base de datos para mejor performance



## Colección Postman
Incluye un archivo challenge_backend.collection con todos los endpoints preconfigurados, incluyendo:

Variables de entorno para base URL y tokens

Tests automáticos para verificar respuestas

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

Variables de entorno
Puedes sobreescribir las variables de entorno al ejecutar el contenedor:

```bash
docker run -d -p 8000:8000 \
  -e DATABASE_URL="postgresql://usuario:password@host:5432/db" \
  -e SECRET_KEY="tu_clave_secreta" \
  --name challenge-api challenge-backend-api

```


  



Especialista en backend Python, FastAPI y automatización avanzada.
