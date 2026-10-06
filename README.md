# English Kids

Website hoc tieng Anh cho tre em tu 3-8 tuoi.

## Tech stack

- Frontend: React, TypeScript, Vite, React Router, Axios
- Backend: Django, Django REST Framework
- Database: MySQL/MariaDB chay bang XAMPP
- API docs: drf-spectacular

## Requirements

- Python 3.12+
- Node.js va npm
- XAMPP voi MySQL/MariaDB

## 1. Cau hinh database

1. Mo XAMPP Control Panel va start MySQL.
2. Mo phpMyAdmin tai `http://localhost/phpmyadmin`.
3. Tao database ten `english_kids` voi charset `utf8mb4`.
4. Kiem tra MySQL dang chay tai `127.0.0.1:3306`.

## 2. Chay backend

Mo terminal tai thu muc `backend`:

```powershell
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Cap nhat `backend/.env` neu tai khoan MySQL cua ban khac mac dinh XAMPP:

```env
SECRET_KEY=your-local-secret-key
DEBUG=True
DB_NAME=english_kids
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```

Kiem tra backend:

- Health: `http://127.0.0.1:8000/api/v1/health/`
- Database health: `http://127.0.0.1:8000/api/v1/health/db/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`

## 3. Chay frontend

Mo terminal moi tai thu muc `frontend`:

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend chay tai `http://127.0.0.1:5173/`.

- Trang chu: `http://127.0.0.1:5173/`
- Trang kiem tra he thong: `http://127.0.0.1:5173/health`

Frontend su dung `VITE_API_URL` trong `frontend/.env` de goi backend.

## 4. Test va build

Backend:

```powershell
cd backend
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test apps.common
```

Frontend:

```powershell
cd frontend
npm run lint
npm run build
```

## Sprint 0 scope

Sprint 0 chi gom project foundation, database connection, health APIs, Swagger, CORS va frontend integration. Authentication, user, course va cac nghiep vu hoc tap se duoc them o cac sprint sau.
"# tienganh" 
