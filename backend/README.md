# English Kids Backend

Backend Django + Django REST Framework cua English Kids.

## Setup

```powershell
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
```

File `.env` can co dang:

```env
SECRET_KEY=your-local-secret-key
DEBUG=True

DB_NAME=english_kids
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```

Can dam bao MySQL/MariaDB cua XAMPP dang chay truoc khi migrate.

## Run

```powershell
python manage.py check
python manage.py runserver 127.0.0.1:8000
```

## Endpoints

- `GET /api/v1/health/`
- `GET /api/v1/health/db/`
- `GET /api/schema/`
- `GET /api/docs/`
- `GET /api/redoc/`

CORS hien chi cho phep frontend `http://localhost:5173`.
