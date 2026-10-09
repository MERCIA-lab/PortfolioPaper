# PortFolio Paper

## 1. Project Tree

```text
portfolio_paper/
├── backend/                              (Django only)
│   ├── manage.py
│   ├── config/                           (settings, urls)
│   │   ├── __init__.py
│   │   ├── settings.py                  (settings, urls)
│   │   └── urls.py
│   ├── apps/
│   │   ├── accounts/                    (users + login)
│   │   ├── portfolio/                  (create, edit, delete)
│   │   └── directory/                  (public list)
│   ├── media/                          (uploaded photos)
│   └── models.py
├── frontend/                            (plain HTML + CSS + JS, no Django)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── form.html
│   ├── directory.html
│   ├── css/
│   └── js/
└── README.md
```

## 2. 3 Layers

### Front-end
Plain HTML + CSS + JS (no Django)

- Landing
- Register/Login
- CV Form
- Directory

```text
fetch request     ───────►     JSON data
   frontend                               backend
```

### Back-end
Django / Python only

- `urls.py` → routes
- `views.py` → application logic
- `forms.py` → validation
- `models.py` → ORM
- `auth`, session handling, validation, JSON API

```text
Frontend  ── request ──>  Backend  ── ORM ──>  Database
    return JSON response ──<───────────────────────
```

### Database
SQLite (dev) / PostgreSQL (prod)

- `users` table
- `portfolio` records
- media/photos stored in `media/`
- SQL query / ORM query

```text
Database
├── users
├── portfolio
├── education
├── experience
├── skills
├── projects
└── media
```

### API routes

- `/api/register/`
- `/api/login/`
- `/api/logout/`
- `/api/portfolio/`  (own CV)
- `/api/directory/`  (all)
- `/api/directory/<slug>/`
- `/api/portfolio/<slug>/`

## 3. Database Design (ERD)

```text
                         1        N
USER ───────────────────────────────────────► PORTFOLIO
PK id                                         PK id
username                                      FK user_id
email                                         full_name
password (hash)                               job_title
date_joined                                   summary
                                              phone / email
                                              location
                                              photo
                                              slug (public URL)
                                              created_at
```

```text
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
created_at
```

```text
               1        N
PORTFOLIO ─────────────────────► EDUCATION
PK id                            PK id
FK portfolio_id                 FK portfolio_id
school                          school
degree                          degree
start / end year                start / end year
```

```text
               1        N
PORTFOLIO ─────────────────────► EXPERIENCE
PK id                            PK id
FK portfolio_id                 FK portfolio_id
company                         company
role                            role
start / end date                start / end date
description                     description
```

```text
               1        N
PORTFOLIO ─────────────────────► SKILL
PK id                            PK id
FK portfolio_id                 FK portfolio_id
name                            name
level (1-5)                     level (1-5)
```

```text
               1        N
PORTFOLIO ─────────────────────► PROJECT
PK id                            PK id
FK portfolio_id                 FK portfolio_id
title                           title
description                     description
link (url)                      link (url)
```

### Entity relationship summary

- `USER` owns one `PORTFOLIO`
- `PORTFOLIO` has many `EDUCATION`, `EXPERIENCE`, `SKILL`, and `PROJECT` rows
- `PK` = primary key
- `FK` = foreign key
- `1` and `N` show cardinality

## 4. System Communication (one request)

```text
(1) FRONT-END              (2) urls.py              (3) views.py
   JS fetch()  ─────────►  route match  ─────►  business logic

(4) models.py              (5) DATABASE
   ORM query ─────────────►  SELECT / PG / SQLite

(6) JSON response ─────►  front-end
       visitor sees the A4 portfolio page
```

### Request flow

1. Front-end sends a request
2. `urls.py` routes the request to the correct view
3. `views.py` handles the logic
4. `models.py` executes ORM query
5. Database returns rows
6. JSON response is sent back to the front-end
7. Visitor sees the final A4-style portfolio page

## 5. User Journey

1. Visit landing page / press Sign Up
2. Register -> user row saved
3. Login -> session cookie created
4. Fill CV form (info, edu, skills, projects)
5. Save -> portfolio + child rows saved in DB
6. Tick `is_public` -> portfolio goes live
7. Portfolio directory lists every public A4 paper

## 6. Notes

- CORS allows the front-end
- passwords hashed (PBKDF2)
- login required on edit API
- only owner can add/delete
- photos saved to `media/`
- directory: searchable + paginated
- slug = public profile URL
- A4 paper view

### A4 paper view

- FULL NAME
- PHOTO
- SUMMARY
- EXPERIENCE
- EDUCATION
- SKILLS

```text
A4 paper view
┌──────────────────────────────────────────┐
│ FULL NAME                                 │
│ PHOTO                                     │
│ SUMMARY                                   │
│ EXPERIENCE                                │
│ EDUCATION                                 │
│ SKILLS                                    │
└──────────────────────────────────────────┘
```

This project is designed as a lightweight portfolio system where users create and publish a public CV page, while administrators or owners manage personal data through a secure Django backend and a simple front-end experience.
