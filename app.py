from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import init_db, SessionLocal
from routers.main_router import main_router

# Initialize FastAPI
app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include main router
app.include_router(main_router, prefix="")


# Database initialization on startup
@app.on_event("startup")
def startup():
    print("Initializing database...")
    init_db()


# Root redirect to documentation or another endpoint
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# OpenAPI debug endpoint (optional, for development only)
@app.get("/openapi-debug", include_in_schema=False)
def debug_openapi():
    from fastapi.openapi.utils import get_openapi

    return get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )


# Database dependency for endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Uvicorn entry point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
