# PortFolio Paper

## 1. Project Tree

```text
portfolio_paper/
├── backend/                               (Django only)
│   ├── manage.py
│   ├── requirements.txt
│   ├── apps/
│   │   ├── accounts/                      (users + login)
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   └── selectors.py
│   │   ├── portfolio/                    (profile + CV content)
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   └── directory/                    (public directory)
│   │       ├── models.py
│   │       ├── views.py
│   │       └── urls.py
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
├── frontend/                              (plain HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   ├── config.js
│   ├── login.html
│   ├── register.html
│   ├── form.html
│   ├── directory.html
│   └── portfolio.html
├── README.md
├── .gitignore
├── LICENSE
├── .env
└── .github/
```

## Run locally

The frontend is plain HTML, CSS and JavaScript. Its API base URL is set in `frontend/config.js`.
The pages expect the Django API from the `backend` branch at `http://localhost:8000/api`.

Run the backend from a backend-branch checkout:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

Run the frontend from the `Front-End` branch in a second terminal:

```bash
git switch Front-End
python3 -m http.server 5500 --directory frontend
```

Open `http://localhost:5500`. The development API allows this origin for session authentication, photo uploads, and CSRF protection.

The sign-in and registration pages use the accounts API. Portfolio details and photos are stored by the backend; only public portfolios appear in the searchable directory, and skills are used as directory tags.

## 2. 3 Layers

```text
FRONT-END
plain HTML + CSS + JS (no Django)
Landing | Register/Login | CV Form | Directory

fetch request  ───────►  JSON data
frontend                  backend

BACK-END
Django / Python only
urls.py -> routes
views.py -> logic
models.py -> ORM
auth, sessions, validation, JSON API

frontend ── request ──> backend ── ORM ──> database
         return JSON response ──<

DATABASE
SQLite (dev) / PostgreSQL (prod)
users | portfolio | education | experience | skills | projects | media/photos
```

## 3. Database Design (ERD)

```text
USER
PK id
username
email
password (hash)
date_joined

PORTFOLIO
PK id
FK user_id
full_name
job_title
summary
phone / email
location
photo
slug (public URL)
is_public
created_at
```

```text
EDUCATION
PK id
FK portfolio_id
school
degree
start / end year
```

```text
EXPERIENCE
PK id
FK portfolio_id
company
role
start / end date
description
```

```text
SKILL
PK id
FK portfolio_id
name
level (1-5)
```

```text
PROJECT
PK id
FK portfolio_id
title
description
link (url)
```

### Relationship summary

```text
USER ──1── owns ──1── PORTFOLIO
PORTFOLIO ──1── has many ──N── EDUCATION
PORTFOLIO ──1── has many ──N── EXPERIENCE
PORTFOLIO ──1── has many ──N── SKILL
PORTFOLIO ──1── has many ──N── PROJECT
```

## 4. System Communication (one request)

```text
(1) FRONT-END       (2) urls.py       (3) views.py
  JS fetch()  ─────►  route match  ─────►  business logic

(4) models.py      (5) DATABASE
  ORM query  ─────►  SELECT / PG / SQLite

(6) JSON response ─────► front-end
    visitor sees the A4 portfolio page
```

### Request flow

1. Front-end sends a request
2. urls.py matches the route
3. views.py handles the logic
4. models.py runs the ORM query
5. database returns rows
6. JSON response is sent back
7. visitor sees the final A4 portfolio page

## 5. User Journey

```text
1. Visit landing page / press Sign Up
2. Register -> user row saved
3. Login -> session cookie created
4. Fill CV form (info, edu, skills, projects)
5. Save -> portfolio + child rows saved in DB
6. Tick is_public -> portfolio goes live
7. Portfolio directory lists every public A4 paper
```

## 6. Notes

- CORS allows the front-end
- passwords hashed (PBKDF2)
- login required on edit API
- only owner can add/delete
- photos saved to media/
- directory: searchable + paginated
- slug = public profile URL
- final view is an A4 portfolio paper

```text
A4 PAPER VIEW
+----------------------------------------+
| FULL NAME                              |
| PHOTO                                  |
| SUMMARY                                |
| EXPERIENCE                             |
| EDUCATION                              |
| SKILLS                                 |
+----------------------------------------+
```

This project is designed as a lightweight portfolio system where users create and publish a public CV page while owners manage their profile through a secure Django backend and a simple front-end experience.
