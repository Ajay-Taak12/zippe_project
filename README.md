## Task Manager API & UI

A full-stack task manager built with **Django + Django REST Framework** on the backend and a **vanilla HTML/JS** single-page UI (`templates/index.html`) on the frontend.

The app supports user registration/login with JWT, and lets authenticated users create, list, filter, paginate, update, and delete their own tasks.

### Features

- **JWT auth**: Register, log in, and get access/refresh tokens.
- **Task CRUD**: Create, list, update, and delete tasks.
- **Pagination**: Page-number pagination with total pages and current page.
- **Filtering & search**:
  - Filter by completed/pending.
  - Full-text search on title and description.
- **Role-based permissions**:
  - Regular users: only see/manage their own tasks.
  - Admins: can see all users and all tasks.
- **Swagger docs**: Auto-generated API docs via Swagger UI.
- **Simple frontend UI**:
  - Register & login forms.
  - Task creation form.
  - Task list with status chips, search, filters, and pagination controls.

---

### Tech Stack

- **Backend**
  - Python 3.10+
  - Django 4.2
  - Django REST Framework 3.14
  - djangorestframework-simplejwt (JWT auth)
  - drf-yasg (Swagger / OpenAPI docs)
  - SQLite (default; can be swapped for PostgreSQL/MySQL)

- **Frontend**
  - Single HTML template: `templates/index.html`
  - Vanilla JavaScript `fetch` calls to the REST API
  - Minimal, responsive CSS inlined in the template

---

### Quick Start

#### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd zippe_project

python -m venv venv
venv\Scripts\activate  # on Windows
# source venv/bin/activate  # on macOS/Linux

pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, it should include at least:

```text
Django>=4.2,<5.0
djangorestframework>=3.14
djangorestframework-simplejwt
drf-yasg
python-dotenv
```

#### 2. Environment variables (optional)

Create a `.env` file in the project root if you want to override defaults:

```env
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
```

#### 3. Run migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 4. Start the development server

```bash
python manage.py runserver
```

Then open the UI in your browser:

- **Frontend UI**: `http://localhost:8000/`
- **Admin panel**: `http://localhost:8000/admin/`
- **Swagger docs**: `http://localhost:8000/swagger/`

---

### API Overview

All API endpoints are prefixed with `/api/`.

#### Auth

- `POST /api/auth/register/`  
  Register a new user.

  **Body (JSON)**:
  ```json
  {
    "username": "john",
    "email": "john@example.com",
    "password": "strong-password",
    "password2": "strong-password"
  }
  ```

- `POST /api/auth/login/`  
  Obtain JWT tokens plus user data.

  **Body (JSON)**:
  ```json
  {
    "username": "john",
    "password": "strong-password"
  }
  ```

  **Response (200)**:
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "user": {
      "id": 1,
      "username": "john",
      "email": "john@example.com",
      "role": "user"
    }
  }
  ```

- `POST /api/auth/token/refresh/`  
  Refresh the access token using a valid refresh token.

- `GET /api/auth/me/`  
  Get details of the currently authenticated user.

#### Tasks

All task endpoints require an `Authorization: Bearer <access_token>` header.

- `GET /api/tasks/`  
  List tasks for the current user (or all tasks if admin).

  **Query params**:
  - `page`: page number (e.g. `?page=2`)
  - `completed`: `"true"` or `"false"` to filter by status
  - `search`: search in `title` and `description`

- `POST /api/tasks/`  
  Create a task.

  **Body (JSON)**:
  ```json
  {
    "title": "My first task",
    "description": "Optional description",
    "completed": false
  }
  ```

- `GET /api/tasks/<id>/`  
  Retrieve a single task.

- `PUT /api/tasks/<id>/`  
  Update a task (full update).

- `PATCH /api/tasks/<id>/`  
  Partial update.

- `DELETE /api/tasks/<id>/`  
  Delete a task.

#### Admin-only User Endpoints

Accessible only to admins (based on `UserProfile.role`):

- `GET /api/users/` – list all users.
- `GET /api/users/<id>/` – retrieve a single user.

---

### Frontend UI Usage

1. **Open** `http://localhost:8000/`.
2. Use the **Register** form to create a new account.
3. Use the **Login** form:
   - On success, the app stores the access token in memory and updates the status bar.
4. In the **Tasks** section:
   - Create tasks via the form.
   - Use:
     - **Filter** dropdown (All / Completed / Pending).
     - **Search** input (title/description).
     - **Previous / Next** buttons for pagination.
   - Toggle task completion or delete tasks via the buttons on each item.

---

### Testing

Basic API tests live in `api/tests.py` and cover:

- User registration and login.
- Creating and listing tasks for an authenticated user.

Run tests with:

```bash
python manage.py test
```

---

### Project Structure (high level)

```text
zippe_project/
├─ api/
│  ├─ models.py         # Task and UserProfile models
│  ├─ views.py          # Auth and task API views
│  ├─ serializers.py    # DRF serializers
│  ├─ urls.py           # API URL routes
│  ├─ pagination.py     # Custom pagination class
│  └─ tests.py          # API tests
├─ zippe_project/
│  ├─ settings.py       # Django settings (REST, JWT, Swagger)
│  └─ urls.py           # Root URL configuration
└─ templates/
   └─ index.html        # Single-page frontend UI
```

---

### Notes

- This project is intended as a simple, educational example of a **JWT-protected Django REST API** plus a **minimal JS frontend**.
- For production use, you should:
  - Set strong, unique `SECRET_KEY` and disable `DEBUG`.
  - Use a robust database (e.g. PostgreSQL).
  - Serve static files via a proper web server or CDN.
  - Add CORS and security hardening as needed.
