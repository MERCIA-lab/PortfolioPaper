# PortfolioPaper

## Project Structure

portfolio_paper/
├── backend/                              (Django only)
│   ├── manage.py
│   ├── requirements.txt
│   ├── apps/
│   │   ├── accounts/                     (users + login)
│   │   ├── portfolio/                   (profile + CV content)
│   │   └── directory/                   (public directory)
│   └── config/
│       ├── settings/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── development.py
│       │   └── production.py
│       ├── __init__.py
│       ├── urls.py
│       ├── asgi.py
│       └── wsgi.py
├── frontend/                             (plain HTML, CSS, JS)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── form.html
│   └── directory.html
├── README.md
├── .gitignore
├── LICENSE
└── .env

## Architecture

Backend
- Django REST API
- user auth and session handling
- portfolio data storage
- public directory endpoints

Frontend
- static HTML pages
- simple form-based client
- fetches JSON from backend

Flow
- Front-end sends requests
- Django routes them
- Backend validates and queries models
- Data is returned as JSON
- Front-end renders the portfolio page
