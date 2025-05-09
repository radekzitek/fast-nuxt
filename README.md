# Fast-Nuxt Project

This project consists of a FastAPI backend and is intended to be used with a Nuxt.js frontend (though the frontend part is not detailed here). The backend provides a robust API for user and team member management and is built with a modern Python stack.

## Backend Overview

The backend is built using FastAPI and provides a RESTful API for managing users and team members, including CRUD operations, password hashing, and data validation. It uses SQLAlchemy as the ORM for database interactions and Alembic for database migrations.

### Backend Features

*   **User Management**:
    *   Create, Read, Update, Delete (CRUD) operations for users.
    *   Secure password hashing using `passlib` (bcrypt).
    *   Data validation using Pydantic models.
    *   Assign users to team members and manage these relationships.
*   **Team Member Management**:
    *   Create, Read, Update, Delete (CRUD) operations for team members.
    *   Self-referential relationships (supervisor/subordinates).
    *   Users can be linked to team members.
*   **Database**:
    *   SQLAlchemy ORM for database interactions.
    *   Alembic for database schema migrations.
    *   SQLite as the default database (configured in `app/core/config.py`).
*   **API**:
    *   Built with FastAPI.
    *   Automatic interactive API documentation (Swagger UI at `/api/v1/docs` and ReDoc at `/api/v1/redoc`).
    *   JWT-based authentication for secure endpoints.
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
│   │   └── endpoints/  # Specific endpoint modules (e.g., users.py, team_members.py)
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
        (If this is the first time and you have no database file, this will create it and set up the schema based on existing migrations.)

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
    *   `POST /login`: Authenticate user and get JWT token.
    *   `POST /token`: OAuth2 password flow for JWT token.
*   **Team Member Endpoints** (prefixed with `/api/v1/team-members`):
    *   `POST /`: Create a new team member.
    *   `GET /`: Get a list of team members.
    *   `GET /{member_id}`: Get a specific team member by ID.
    *   `PUT /{member_id}`: Update a team member by ID.
    *   `DELETE /{member_id}`: Delete a team member by ID.

---

## Frontend Overview

The frontend is built with Vite and Vue 3, using the Vuetify UI library for a modern, responsive interface. It provides user and team member management features, interacting with the FastAPI backend via RESTful API calls.

### Frontend Features

- User CRUD operations with dialogs for create/edit and detail views
- Team member CRUD operations, including supervisor relationships
- Assigning users to team members and vice versa
- Search and filtering in data tables
- Responsive design with Vuetify components
- API error handling and feedback

### Frontend Tech Stack

- **Framework:** Vue 3
- **UI Library:** Vuetify
- **Build Tool:** Vite
- **State Management:** Pinia (if used)
- **Routing:** Vue Router
- **HTTP Client:** Axios

### Frontend Project Structure

The frontend code is organized within the `frontend/ui/` directory:

```
frontend/ui/
├── public/           # Static assets (favicon, etc.)
├── src/              # Main source code
│   ├── assets/       # Images, logos, etc.
│   ├── components/   # Reusable Vue components
│   ├── layouts/      # Layout components
│   ├── pages/        # Page components (e.g., users.vue, team.vue, aiph.vue)
│   ├── plugins/      # Vue plugins
│   ├── router/       # Vue Router configuration
│   ├── stores/       # Pinia stores (if used)
│   ├── styles/       # Global and component styles
│   ├── App.vue       # Root Vue component
│   └── main.js       # Entry point
├── package.json      # Project metadata and dependencies
├── vite.config.mjs   # Vite configuration
└── README.md         # Frontend-specific documentation
```

### Frontend Setup and Running

1. **Prerequisites:**
    - Node.js (v16+ recommended)
    - pnpm (or npm/yarn)

2. **Navigate to the frontend directory:**
    ```bash
    cd frontend/ui
    ```

3. **Install dependencies:**
    ```bash
    pnpm install
    # or
    npm install
    # or
    yarn install
    ```

4. **Run the development server:**
    ```bash
    pnpm dev
    # or
    npm run dev
    # or
    yarn dev
    ```
    The app will be available at `http://localhost:3000` by default.

5. **Configuration:**
    - The frontend expects the backend API to be running at `http://localhost:8000` (see axios base URLs in the code).
    - Adjust API URLs in the code or use environment variables as needed for deployment.

### Frontend Usage

- Navigate to `/users` to manage users.
- Navigate to `/team` to manage team members.
- Use the plus (+) button in the users list to quickly create and assign a team member.
- Deleting a team member will automatically unassign any users linked to that team member.

---

*For more details, see the `frontend/ui/README.md`.*
