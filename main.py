from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from database import Base, engine, run_auto_migrations
import models  # noqa: F401 - needed so SQLAlchemy registers the models before create_all
from orders_router import router as orders_router, menu_router

# Create tables on startup (fine for dev; use Alembic migrations for production)
Base.metadata.create_all(bind=engine)

# Add any new columns to existing tables so you don't need to delete fetchit.db
# every time the order/menu structure changes.
run_auto_migrations()

app = FastAPI(title="Fetchit POS")

# Allow the frontend (pos.html, opened directly in the browser) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router)
app.include_router(menu_router)


@app.get("/")
def root():
    return FileResponse("pos.html")


@app.get("/api-status")
def api_status():
    return {"status": "Fetchit POS API running"}