# Architecture

## Goal

Build a simple MVP that is free to run and easy to understand. The application runs locally on one computer. It is suitable for learning, demonstrating the workflow, and a small local team trial.

## Simple free stack

| Area | Choice | Why |
| --- | --- | --- |
| Programming language | Python 3.12 | The application language; familiar, readable, and well supported by Streamlit |
| Application and user interface | Streamlit | One application instead of a separate frontend and backend |
| Database | PostgreSQL 17 in Docker (`pgvector/pgvector:pg17`) | Free, reliable for concurrent users, and ready for later deployment |
| Database access | SQLAlchemy + a PostgreSQL driver | Keeps database queries in Python and avoids a future SQLite-to-PostgreSQL migration |
| Container orchestration | Docker Compose | Starts Streamlit and PostgreSQL together with one command, locally and later in deployment |
| Scheduling | Checks made when the app is opened | No paid or separate scheduler service |
| Deployment | Local computer | Free and private; no hosting bill |

## Python packages

The first version keeps dependencies intentionally small:

| Package | Purpose |
| --- | --- |
| `streamlit` | Builds the complete web interface and runs the application |
| `SQLAlchemy` | Defines database models and performs PostgreSQL queries from Python |
| `psycopg[binary]` | PostgreSQL database driver used by SQLAlchemy |
| `alembic` | Tracks and applies database-schema changes safely as the application evolves |

Python's standard library covers the remaining initial needs: `datetime` and `zoneinfo` for weekly deadlines and project timezones; `os` for configuration; and `secrets`/`hashlib` for the simple local login approach.

The project does not need FastAPI, Redis, Celery, a separate `pgvector` Python package, or an email package for the initial local MVP.

## System shape

```text
Browser
  |
  v
Docker Compose
  |-- Streamlit application
  `-- PostgreSQL Docker container
```

There is no FastAPI service, hosted database, Redis instance, or cloud scheduler in this first version. Docker Compose manages the Streamlit and PostgreSQL containers together, while Streamlit remains the only application service.

## Running the app

The person running the project starts the local application with Docker Compose, which starts PostgreSQL before Streamlit. They then open the Streamlit URL in a browser. PostgreSQL listens on `localhost:5432` when its container is running.

The Compose file holds the service definitions, container image versions, internal networking, and non-secret configuration. Database passwords and other secrets are supplied through a local environment file that is not committed to Git.

For a small team on the same network, Streamlit can later be made available on that local network. It should not be exposed to the public internet without adding proper authentication, HTTPS, and a production deployment setup.

## Users and roles

The MVP has two project roles:

- **Manager:** creates a project, manages team members, views feedback, and records decisions and action items.
- **Team member:** submits and edits their own feedback while the weekly cycle is open.

For the first local version, use a simple login approach suitable for a demo or trusted local users. This is not production-grade identity management. A future hosted version can replace it with proper authentication without changing the basic feedback workflow.

## Core data

PostgreSQL contains these main tables:

| Table | Purpose |
| --- | --- |
| `users` | People who can use the local application |
| `projects` | Projects and their timezone and retrospective settings |
| `project_members` | A user's role in a project |
| `weekly_cycles` | The current feedback period for each project |
| `feedback_submissions` | Structured feedback from a member for a cycle |
| `retrospectives` | Meeting record for a cycle |
| `decisions` | Decisions made during the retrospective |
| `action_items` | Follow-up work, including description, owner, and deadline |

Each feedback submission has an internal `author_id` and an `is_anonymous` flag. The author ID lets a member edit their own submission before closure. When feedback is anonymous, manager views display no author name.

## Weekly-cycle rules

The application calculates whether feedback is open from the project timezone and the current time.

| Time | Rule |
| --- | --- |
| Monday to Friday 10:00 | Team members may submit or edit feedback |
| Friday 10:00 onwards | Feedback is closed; no create or edit actions are accepted |
| Retrospective time | Manager reviews the feedback board and records decisions/action items |
| After retrospective | The completed weekly cycle and its related data are deleted |

These rules are checked whenever a user opens the application or takes an action. For example, if somebody opens the app after Friday 10:00, they cannot submit feedback even if the app was not open precisely at 10:00.

## Reminders and cleanup

There is no automatic email or scheduled reminder service in the free local version.

- The application shows a visible reminder message when a user opens it on Wednesday, Thursday, or Friday morning without having submitted feedback.
- The manager can send a manual reminder outside the app—for example by email or a team chat message.
- Cleanup runs the next time the application is opened after the retrospective time. It removes the completed cycle, its feedback, retrospective record, decisions, and action items.

This is intentionally simpler than a hosted scheduler. If reliable automated reminders later become essential, that is the point to add a deployed scheduler and likely a small hosting cost.

## Streamlit pages

- **Login:** select or sign in as a local user.
- **Project:** choose the active project.
- **My feedback:** submit or edit the structured weekly feedback form; choose anonymous or attributed submission.
- **Manage members:** manager-only page for team membership.
- **Feedback board:** manager-only grouped view of what worked, blockers, improvements, suggestions, and other feedback.
- **Retrospective:** manager-only decisions and action items.

## Privacy and limitations

Anonymous feedback hides author names in the manager-facing feedback board. However, this local MVP is not designed to provide strong anonymity against a person who has direct access to the PostgreSQL database or the application source code.

This version is deliberately limited:

- No cloud hosting or public URL.
- No automated email reminders.
- No production-grade authentication or backups.
- No historical feedback, analytics, AI features, or chat integrations.

Those exclusions keep the project free, understandable, and focused on validating the weekly feedback workflow.

## Future upgrade path

Once the simple workflow is working, use Docker Compose as the deployment baseline: deploy the Streamlit container and either the PostgreSQL container or a managed PostgreSQL provider. A public deployment still needs real multi-user authentication, reliable scheduled reminders, backups, and stronger privacy controls. The user roles, feedback fields, and weekly-cycle rules can remain the same.
