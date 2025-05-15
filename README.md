# Backend Service

🚀 This is backend for most of my projects built using FastAPI and PostgreSQL.
🐳 For Dockerized version, visit [backend-docker](https://github.com/Anktw/backenddocker)`

![image](https://github.com/user-attachments/assets/8c292a9c-41af-4289-a2b3-e31bb3904a8a)


## Quick Start

1. 📋 Clone repository -> 
```git clone https://github.com/Anktw/backend.git```
2. 📦 Install dependencies:
```pip install -r requirements.txt```
3. 🔑 Setup environment variables -> rename env.example to .env and fill the values
```cp env.example .env```
4. Create a database in PostgreSQL (recommended name `backend`)
5. 🏗️ Run migrations
```alembic revision --autogenerate -m "Initial migration"```
```alembic upgrade head```
6. 🏃 Run the app
```fastapi dev app/main.py```

## Features
- 🚀 FastAPI framework
- 🗄️ PostgreSQL database
- 📦 Redis

## Deployment
After deployment, run migrations in console of your server
```alembic revision --autogenerate -m "Initial migration"```
```alembic upgrade head```
Some cloud providers

- Koyeb - [https://www.koyeb.com/](https://www.koyeb.com/)(Recommended)
- Render - [https://render.com/](https://render.com/)
- Railway - [https://railway.app/](https://railway.app/)
- Sevalla - [https://app.sevalla.com/](https://app.sevalla.com/)

For PostgreSQL, you can use
- Neon - [https://neon.tech/](https://neon.tech/) (Recommended)

## Acknowledgements
-  FastAPI - [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
-  PostgreSQL - [https://www.postgresql.org/](https://www.postgresql.org/)
-  Redis - [https://redis.io/](https://redis.io/)
-  Pydantic - [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
-  SQLAlchemy - [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
-  Uvicorn - [https://www.uvicorn.org/](https://www.uvicorn.org/)
-  Argon2 - [https://github.com/hynek/argon2-cffi](https://github.com/hynek/argon2-cffi)
-  Authlib - [https://authlib.org/](https://authlib.org/)
-  Email Validator - [https://github.com/defuz/email-validator](https://github.com/defuz/email-validator)
-  Starlette - [https://www.starlette.io/](https://www.starlette.io/)
-  Typer - [https://typer.tiangolo.com/](https://typer.tiangolo.com/)
-  alembic - [https://alembic.sqlalchemy.org/](https://alembic.sqlalchemy.org/)

## License
MIT License

---

## Author
Made with ❤️ by [Unkit](https://github.com/Anktw)
