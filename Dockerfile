FROM python:3.13

WORKDIR /app

RUN mkdir -p /app

RUN mkdir -p /app/core

COPY /core/* /app/core

RUN mkdir -p /app/db

COPY /db/* /app/db

RUN mkdir -p /app/middleware

COPY /middleware/* /app/middleware

RUN mkdir -p /app/models

COPY /models/* /app/models

RUN mkdir -p /app/routers

COPY /routers/* /app/routers

RUN mkdir -p /app/schemas

COPY /schemas/* /app/schemas

RUN mkdir -p /app/alembic

COPY /alembic/* /app/alembic

COPY /main.py /app/main.py

COPY alembic.ini /app/alembic.ini

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]

