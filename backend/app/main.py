"""
Main FastAPI Application.

This module initializes the FastAPI application, includes API routers,
and defines startup and shutdown event handlers. It serves as the
primary entry point for the ASGI server (e.g., Uvicorn).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from app.api import api_router  # Main API router
from app.db.session import engine  # SQLAlchemy engine
from app.db.base_class import Base  # SQLAlchemy declarative base for table creation
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta

# This is optional: Create tables if they don't exist (for development)
# For production, you should rely on Alembic migrations for schema management.


def create_db_and_tables():
    """
    Creates all database tables defined by SQLAlchemy models.

    This function is intended for development convenience to quickly set up
    the database schema. In a production environment, Alembic migrations
    should be used for managing database schema changes.
    """
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AIPH Backend API",
    description="""
    ## Fast-Nuxt API

    This API provides endpoints for:
    - User management (CRUD, authentication)
    - Team member management (CRUD)
    - JWT-based authentication

    ### Authentication
    - Obtain a JWT token via `/api/v1/users/token` (OAuth2 password flow)
    - Use the token as a Bearer token in the `Authorization` header for protected endpoints

    ### Main Endpoints
    - `/api/v1/users/` - User CRUD
    - `/api/v1/team-members/` - Team member CRUD

    ### Notes
    - All endpoints return JSON
    - All endpoints are documented below
    """,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
)
"""
The main FastAPI application instance.
Configured with a title, description, and version for the API documentation.
"""

# Define allowed origins for CORS
# In a production environment, you should restrict this to your actual frontend domain.
# For development, allowing localhost with common ports is typical.
origins = [
    "http://localhost",
    "http://localhost:3000",  # Common Nuxt.js dev port
    "http://localhost:8080",  # Other common dev ports
    "http://localhost:5173",  # Common Vite dev port
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,  # Allow cookies to be included in requests
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.on_event("startup")
def on_startup():
    """
    Application startup event handler.

    This function is executed when the FastAPI application starts up.
    It can be used to initialize resources, such as database connections,
    or perform other setup tasks. Currently, it prints a startup message.
    The `create_db_and_tables()` call is commented out, as Alembic is preferred.
    """
    # You might want to remove this for production and use Alembic exclusively
    # create_db_and_tables() # Example: creates tables on startup if not using Alembic
    print("Application startup complete.")
    # You could also initialize DB connection pools or other resources here


@app.on_event("shutdown")
def on_shutdown():
    """
    Application shutdown event handler.

    This function is executed when the FastAPI application is shutting down.
    It can be used to clean up resources, such as closing database connections.
    Currently, it prints a shutdown message.
    """
    print("Application shutdown.")
    # Clean up resources, e.g., close DB connection pools


# Include the main API router with a version prefix
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint of the API.

    Provides a simple welcome message.

    Returns:
        dict: A dictionary with a welcome message.
    """
    return {"message": "Welcome to the FastAPI Nuxt Backend!"}


# If you want to run this directly using `python app/main.py` (though uvicorn is preferred for development and production)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
