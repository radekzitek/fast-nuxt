# Fast-Nuxt Project

This project consists of a FastAPI backend and is intended to be used with a Nuxt.js frontend (though the frontend part is not detailed here). The backend provides a robust API for user management and is built with a modern Python stack.

## Backend Overview

The backend is built using FastAPI and provides a RESTful API for managing users, including CRUD operations, password hashing, and data validation. It uses SQLAlchemy as the ORM for database interactions and Alembic for database migrations.

### Backend Features

*   **User Management**:
    *   Create, Read, Update, Delete (CRUD) operations for users.
    *   Secure password hashing using `passlib` (bcrypt).
    *   Data validation using Pydantic models.
*   **Database**:
    *   SQLAlchemy ORM for database interactions.
    *   Alembic for database schema migrations.
    *   SQLite as the default database (configured in `app/core/config.py`).
*   **API**:
    *   Built with FastAPI.
    *   Automatic interactive API documentation (Swagger UI at `/docs` and ReDoc at `/redoc` under the API version prefix).
    *   Clear separation of concerns with routers, schemas (Pydantic models), CRUD operations, and ORM models.

### Backend Tech Stack

*   **Framework**: FastAPI
*   **ASGI Server**: Uvicorn
*   **ORM**: SQLAlchemy
*   **Database Migrations**: Alembic
*   **Data Validation/Serialization**: Pydantic
*   **Password Hashing**: Passlib
*   **Configuration Management**: Pydantic-Settings (via `.env` file)
*   **Database**: SQLite (default)

### Backend Project Structure

The backend code is organized within the `backend/` directory:

```
backend/
├── alembic/            # Alembic migration scripts and configuration
├── alembic.ini         # Alembic configuration file
├── app/                # Main application package
│   ├── __init__.py
│   ├── api/            # API endpoints (routers)
│   │   ├── __init__.py
│   │   └── endpoints/  # Specific endpoint modules (e.g., users.py)
│   ├── core/           # Core logic (config, security)
│   ├── crud/           # CRUD operations (database interactions)
│   ├── db/             # Database setup (SQLAlchemy base, session)
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic schemas for data validation
│   └── main.py         # FastAPI application instance and main router
├── data/               # Directory for SQLite database file (e.g., fast-nuxt.db)
├── requirements.txt    # Python dependencies
└── .env.example        # Example environment variables file (create .env from this)
```

### Backend Setup and Running

1.  **Prerequisites**:
    *   Python 3.8+
    *   `pip`

2.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

3.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up environment variables**:
    *   Copy `.env.example` to `.env` (if it exists and you need to customize, otherwise the defaults in `app/core/config.py` will be used).
    *   The default `SQLALCHEMY_DATABASE_URL` in `app/core/config.py` points to `sqlite:///./data/fast-nuxt.db`. The `data/` directory will be created if it doesn't exist when the app first tries to access the DB or when migrations run.

6.  **Database Migrations**:
    *   Ensure your database URL is correctly configured (either in `.env` or `app/core/config.py`).
    *   Apply Alembic migrations to create the database tables:
        ```bash
        alembic upgrade head
        ```
        (If this is the first time and you have no database file, this will create it and set up the schema based on existing migrations like `96ed129e40eb_create_initial_tables_incl_users.py`.)

7.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

### Backend API Endpoints

*   **API Docs**:
    *   Swagger UI: `http://127.0.0.1:8000/api/v1/docs`
    *   ReDoc: `http://127.0.0.1:8000/api/v1/redoc`
*   **User Endpoints** (prefixed with `/api/v1/users`):
    *   `POST /`: Create a new user.
    *   `GET /`: Get a list of users.
    *   `GET /{user_id}`: Get a specific user by ID.
    *   `PUT /{user_id}`: Update a user by ID.
    *   `DELETE /{user_id}`: Delete a user by ID.

---

*This README provides an overview based on the backend structure. Further details for the Nuxt.js frontend would be added separately.*
