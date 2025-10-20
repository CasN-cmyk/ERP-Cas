import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.db import Base, engine
from .routers import auth, crm, customers, finance, integrations, orders, products, purchase, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app_settings = get_settings()
app = FastAPI(title=app_settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(customers.router)
app.include_router(purchase.router)
app.include_router(finance.router)
app.include_router(crm.router)
app.include_router(settings.router)
app.include_router(integrations.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
