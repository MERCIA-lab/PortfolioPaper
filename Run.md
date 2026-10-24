# Run Portfolio Paper

This project has a Django REST API backend and a static HTML/CSS/JavaScript frontend. For local development, run them in two separate terminals.

## Requirements

- Windows with PowerShell
- Python 3.12 or newer

The backend uses SQLite for local development, so no separate database server is needed.

## 1. Set up and start the backend

From the repository root, run these commands in PowerShell:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API will be available at <http://localhost:8000/>. The API root is <http://localhost:8000/api/> and lists the main account, portfolio, and directory endpoints.

Keep this terminal running while using the application.

### Optional: create an admin account

To use the Django admin, stop the server with `Ctrl+C`, then run:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Open <http://localhost:8000/admin/> and sign in with the account you created.

## 2. Start the frontend

Open a second PowerShell terminal from the repository root and run:

```powershell
cd frontend
py -m http.server 5500
```

Open <http://localhost:5500/> in your browser. Use the site navigation to register or sign in, create a portfolio, and explore the public directory.

The frontend's API address is set to `http://localhost:8000/api` in `frontend/config.js`. The development backend is configured to accept requests from the frontend's local port, so keep the default ports unless you also update the frontend API address and backend CORS settings.

## Start both services in VS Code

After installing the dependencies and applying migrations, run **Terminal > Run Task > Run PortfolioPaper (frontend + backend)** to start both servers. Open <http://localhost:5500/> to use the application. When signed in, choose **Sign out** in the header; the sign-in page will let you get back in.

## Database and uploaded files

The development settings use SQLite. Django creates or updates the database at `backend/db.sqlite3` when migrations are applied. Uploaded media is stored under the backend media directory during development.

## Troubleshooting

- **`py` is not recognized:** Install Python and enable the Python launcher, or replace `py` in the commands with `python`.
- **PowerShell blocks virtual-environment activation:** Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate the environment again.
- **The frontend loads but API requests fail:** Make sure both servers are running, the backend is on port `8000`, and the frontend is served on port `5500` (not opened directly as a file).
- **The database reports pending migrations:** Stop the backend and run `python manage.py migrate` from the `backend` directory, then restart it.
