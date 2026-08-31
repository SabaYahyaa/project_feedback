# Architecture

## Goal

Build a simple MVP that is free to run and easy to understand. The application runs locally on one computer. It is suitable for learning, demonstrating the workflow, and a small local team trial.

## Simple free stack

| Area | Choice | Why |
| --- | --- | --- |
| Application and user interface | Streamlit + Python | One application instead of a separate frontend and backend |
| Database | PostgreSQL 17 in Docker (`pgvector/pgvector:pg17`) | Free, reliable for concurrent users, and ready for later deployment |
| Database access | SQLAlchemy + a PostgreSQL driver | Keeps database queries in Python and avoids a future SQLite-to-PostgreSQL migration |
| Scheduling | Checks made when the app is opened | No paid or separate scheduler service |
| Deployment | Local computer | Free and private; no hosting bill |

## System shape

```text
Browser
  |
  v
Streamlit application
  |
  v
PostgreSQL Docker container
```

There is no FastAPI service, hosted database, Redis instance, or cloud scheduler in this first version. Keeping the application in one Streamlit service makes the codebase much smaller and easier to follow. PostgreSQL runs locally in Docker and is accessed only by Streamlit.

## Running the app

The person running the project starts the local PostgreSQL Docker container, then starts Streamlit and opens the local application URL in a browser. PostgreSQL listens on `localhost:5432` when the Docker container is running.

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

Once the simple workflow is working, deploy the existing PostgreSQL schema to a managed PostgreSQL provider and host Streamlit only if you need public access, real multi-user authentication, reliable scheduled reminders, backups, or stronger privacy controls. The user roles, feedback fields, and weekly-cycle rules can remain the same.
