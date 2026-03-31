import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from starlette.middleware.sessions import SessionMiddleware

from database import Base, engine
from routers import receipts


SESSION_SECRET = os.getenv("SESSION_SECRET")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"

if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET is required. Set it in .env before starting the app.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE receipts ADD COLUMN IF NOT EXISTS receipt_date DATE"))
        conn.execute(text("ALTER TABLE receipts ADD COLUMN IF NOT EXISTS is_expense BOOLEAN NOT NULL DEFAULT TRUE"))
        conn.execute(text("ALTER TABLE receipts ADD COLUMN IF NOT EXISTS stored_filename VARCHAR(255)"))
        conn.execute(text("ALTER TABLE receipts ADD COLUMN IF NOT EXISTS image_data BYTEA"))
        conn.execute(text("ALTER TABLE receipts ADD COLUMN IF NOT EXISTS image_content_type VARCHAR(50)"))
        conn.commit()
    yield


app = FastAPI(title="経費管理Webアプリ", lifespan=lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=COOKIE_SECURE,
    max_age=60 * 60 * 12,
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.get("/health")
async def healthcheck():
    return PlainTextResponse("ok")


app.include_router(receipts.router)
