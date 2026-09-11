# QueueKub

Online queue booking system (similar to QueQ) built with Django. Customers browse
shops and join a queue online; shop owners manage the queue from a dashboard;
admins manage the system via Django Admin.

## Status: Sprint 1 — Foundation (complete)

Sprint 1 delivers the project foundation: project setup, authentication with
roles, and shop management (CRUD, list, search, detail). The queue system
itself (join/call-next/skip/complete) is Sprint 2 work and is not built yet —
`queues` and `dashboard` are scaffolded as empty apps ready for that work.

**Sprint 1 Definition of Done** (verified working):
Register → Login → Owner creates a shop → Customer/anonymous visitor sees the
shop in the list → Customer opens the shop detail page.

## Tech Stack

- Backend: Django 5.2
- Frontend: Django Templates + Bootstrap 5
- Database: PostgreSQL
- Auth: Django's built-in authentication + a custom `User` model with roles
  (`CUSTOMER`, `OWNER`, `ADMIN`)

## Project Structure

```
QueueKub/
├── config/         # Project settings, root urls, home view
├── accounts/       # Custom User model, register/login/logout, roles
├── shops/          # Shop model, CRUD, list, search, detail
├── queues/         # (Sprint 2) Queue model & business logic
├── dashboard/      # (Sprint 2/3) Shop owner dashboard & statistics
├── templates/       # Shared templates (base.html, home.html, per-app templates)
├── static/         # CSS/JS
├── media/          # User-uploaded files (gitignored)
├── manage.py
└── requirements.txt
```

## Local Setup

1. **Clone and create a virtualenv**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create a PostgreSQL database**

   ```bash
   sudo -u postgres psql -c "CREATE USER queuekub WITH PASSWORD 'queuekub_dev_pw' CREATEDB;"
   sudo -u postgres psql -c "CREATE DATABASE queuekub OWNER queuekub;"
   ```

3. **Configure environment variables**

   Copy `.env.example` to `.env` and adjust values as needed:

   ```bash
   cp .env.example .env
   ```

   | Variable | Description |
   | --- | --- |
   | `SECRET_KEY` | Django secret key — use a long random string |
   | `DEBUG` | `True` for local development, `False` in production |
   | `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
   | `DATABASE_URL` | e.g. `postgres://queuekub:queuekub_dev_pw@localhost:5432/queuekub` |

   `.env` is gitignored — never commit real secrets.

4. **Run migrations and start the server**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/`.

5. **Run tests**

   ```bash
   python manage.py test
   ```

## User Roles

- **Customer** — registers, browses/searches shops, views shop details.
- **Shop Owner** — registers with the "Shop Owner" role, creates and manages
  their own shops (`/shops/create/`, `/shops/mine/`).
- **Admin** — any Django superuser automatically gets the `ADMIN` role and can
  manage everything via `/admin/`.

## Deployment (Render / Railway)

The app is deploy-ready:

- `Procfile` defines a `web` process (`gunicorn`) and a `release` step
  (`migrate`).
- `whitenoise` serves static files in production (`DEBUG=False`).
- All secrets/config come from environment variables (`DATABASE_URL`,
  `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG`).

Steps:

1. Provision a PostgreSQL database on the platform and note its `DATABASE_URL`.
2. Set environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`,
   `DATABASE_URL`, `CSRF_TRUSTED_ORIGINS` (your deployed domain).
3. Deploy — the `release` step runs migrations automatically; run
   `python manage.py collectstatic --noinput` as part of the build step.
4. Create a superuser with `python manage.py createsuperuser` (via the
   platform's shell/console).

## Roadmap

- **Sprint 2 — Core Queue**: Queue model, join/cancel queue, call next/skip/
  complete, estimated waiting time, queue validation.
- **Sprint 3 — Polish + Production**: customer/shop dashboards, queue
  history, statistics, responsive UI polish, testing, deployment.
- **Advanced (post-MVP)**: realtime updates (Django Channels), notifications,
  QR code check-in, analytics, reservations.
