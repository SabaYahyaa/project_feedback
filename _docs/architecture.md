# Architecture

## Goal

Build a simple MVP that is free to run locally, easy to understand, and ready for real multi-user use later. The application runs on one computer first, using Django's built-in tools for login, forms, database access, and administration.

## Simple free stack

| Area | Choice | Why |
| --- | --- | --- |
| Programming language | Python 3.12 | Readable application language with strong Django support |
| Web application and user interface | Django templates | One application provides pages, forms, login, permissions, and server-side rules |
| Database | PostgreSQL 17 in Docker (`pgvector/pgvector:pg17`) | Free, reliable for concurrent users, and ready for later deployment |
| Database access | Django ORM | Django's built-in model and query layer; no separate ORM is required |
| Database migrations | Django migrations | Creates and updates tables from Django models; no manual SQL table creation is needed |
| Administration | Django admin | Lets the manager create and manage test users and data during development |
| Container orchestration | Docker Compose | Starts Django and PostgreSQL together with one command, locally and later in deployment |
| Scheduling | Checks made when a page is requested | No paid scheduler service for the local MVP |
| Deployment | Local computer | Free and private while the MVP is tested |

## Python packages

The first version keeps dependencies intentionally small:

| Package | Purpose |
| --- | --- |
| `Django` | Web pages, forms, authentication, permissions, ORM, migrations, and admin site |
| `psycopg[binary]` | Python driver that connects Django to PostgreSQL |
| `pytest` | Runs automated tests |
| `pytest-django` | Makes Django models, pages, and test database tools available to pytest |

Python's standard library provides `datetime` and `zoneinfo` for weekly deadlines and project timezones, plus `os` for environment-based configuration. The initial MVP does not need Streamlit, FastAPI, SQLAlchemy, Alembic, Redis, Celery, a separate `pgvector` Python package, or an email package.

## System shape

```text
Browser
  |
  v
Docker Compose
  |-- Django application
  `-- PostgreSQL Docker container
```

Django is the only application service. It renders the web pages, applies all permission and weekly-cycle rules, and uses PostgreSQL to store data.

## Running the app

Docker Compose starts the PostgreSQL container and Django application together. The user opens Django in a browser; PostgreSQL listens on `localhost:5432` when its container is running.

The Compose file holds service definitions, image versions, internal networking, and non-secret configuration. Database passwords, Django's secret key, and other secrets are provided through a local environment file that is not committed to Git.

For a small team on the same network, Django can later be made available on that local network. It should not be exposed to the public internet without HTTPS, secure production settings, backups, and a production deployment setup.

## Users and roles

Django's built-in `User` model provides login, secure password hashing, and sessions. Project access is controlled with a project-membership model rather than a complex global role system.

- **Manager:** creates a project, manages project members, views feedback, and records decisions and action items.
- **Team member:** submits and edits their own feedback while the weekly cycle is open.

A user must be a member of a project before accessing its data. Django views check the current logged-in user and that user's role for the selected project before allowing an action.

## Core data

PostgreSQL contains these main models and tables:

| Model | Purpose |
| --- | --- |
| Django `User` | Authenticated people using the application |
| `Project` | A project, including its timezone and retrospective settings |
| `ProjectMembership` | A user's manager or team-member role within a project |
| `WeeklyCycle` | The current feedback period for a project |
| `FeedbackSubmission` | Structured feedback from a member for a cycle |
| `Retrospective` | Meeting record for a cycle |
| `Decision` | A decision recorded during a retrospective |
| `ActionItem` | Follow-up work with description, owner, and deadline |

Each feedback submission has an internal author relationship and an `is_anonymous` flag. The author relationship lets a member edit their own submission before closure, while manager-facing pages display no author name for anonymous feedback.

## Weekly-cycle rules

Django calculates whether feedback is open from the project timezone and the current server time.

| Time | Rule |
| --- | --- |
| Monday to Friday 10:00 | Team members may submit or edit feedback |
| Friday 10:00 onwards | Feedback is closed; create and edit requests are rejected by Django |
| Retrospective time | Manager reviews the feedback board and records decisions/action items |
| After retrospective | The completed weekly cycle and its related data are deleted |

The rules are checked every time a relevant Django view receives a request. A page cannot rely only on hiding a button; the server must reject an action after the deadline.

## Reminders and cleanup

There is no automatic email or scheduled reminder service in the free local version.

- Django displays a reminder message to a member who visits the app on Wednesday, Thursday, or Friday morning without submitting feedback.
- The manager can send manual reminders outside the app, for example through email or team chat.
- Cleanup runs safely when the application receives a request after the retrospective time. It removes the completed cycle, feedback, retrospective, decisions, and action items.

If reliable automatic reminders or exact timed cleanup later become essential, add a deployed scheduler and likely a small hosting cost.

## Django pages

- **Login and logout:** Django's authentication pages.
- **Project dashboard:** current cycle, deadline, role-appropriate navigation, and reminder messages.
- **My feedback:** team-member form for creating or editing structured feedback and choosing anonymity.
- **Project members:** manager-only membership management.
- **Feedback board:** manager-only grouped feedback view that respects anonymity.
- **Retrospective:** manager-only decisions and action items.
- **Django admin:** development and manager support for users and application data.

## Privacy and limitations

Anonymous feedback hides author names in manager-facing pages. This local MVP does not provide strong anonymity against a person with direct PostgreSQL database or source-code access.

This version is deliberately limited:

- No cloud hosting or public URL.
- No automated email reminders.
- No historical feedback, analytics, AI features, or chat integrations.
- No production backup, monitoring, or operational guarantees.

Those exclusions keep the project free, understandable, and focused on validating the weekly feedback workflow.

## Future deployment path

Docker Compose remains the deployment baseline. Deploy the Django container and either the PostgreSQL container or a managed PostgreSQL provider when public access is needed.

Before public deployment, configure HTTPS, secure Django production settings, environment-managed secrets, reliable backups, a scheduler for timed automation, and stronger privacy controls. The user roles, feedback fields, and weekly-cycle rules can remain the same.
