from fastapi import FastAPI
from app.api import api_router # Corrected import
from app.db.session import engine # To create tables if they don't exist
from app.db.base_class import Base # To access metadata for table creation

# This is optional: Create tables if they don't exist (for development)
# For production, you should rely on Alembic migrations.
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Nuxt Backend",
    description="API for the Fast-Nuxt project",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    # You might want to remove this for production and use Alembic exclusively
    # create_db_and_tables()
    print("Application startup complete.")
    # You could also initialize DB connection pools or other resources here

@app.on_event("shutdown")
def on_shutdown():
    print("Application shutdown.")
    # Clean up resources, e.g., close DB connection pools

app.include_router(api_router, prefix="/api/v1") # Add a version prefix

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Nuxt Backend!"}

# If you want to run this directly using `python app/main.py` (though uvicorn is preferred)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)