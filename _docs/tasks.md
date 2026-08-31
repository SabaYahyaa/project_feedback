# Backlog

## 1. Create the empty project and passing test
Goal: Establish a runnable Python project with one automated test that passes.
Description: Create the initial project structure, dependency definition, and test configuration for the Streamlit application. Add one minimal test that can be run locally and passes, without implementing product functionality.

## 2. Define local environment configuration
Goal: Define how the application receives local, non-secret configuration.
Description: Document and prepare the environment variables needed by the application, including the PostgreSQL connection string and local application settings. Ensure secrets are read from a local environment file that is excluded from Git, with a safe example file for developers.

## 3. Add Docker Compose services
Goal: Run the application and PostgreSQL together through Docker Compose.
Description: Define a Compose setup with a Streamlit service and a PostgreSQL 17 service using the `pgvector/pgvector:pg17` image. Configure service networking, persistent PostgreSQL storage, environment variables, and local ports without placing credentials in version control.

## 4. Connect Python to PostgreSQL
Goal: Provide one tested database connection for the Streamlit application.
Description: Configure SQLAlchemy and the `psycopg` PostgreSQL driver to create database sessions from the application configuration. Include a small connectivity check and clear error handling when PostgreSQL is unavailable.

## 5. Set up database migrations
Goal: Manage PostgreSQL schema changes with Alembic.
Description: Initialize Alembic for the project and configure it to use the same PostgreSQL connection settings as the application. Add a documented workflow for creating and applying future schema migrations.

## 6. Create user, project, and membership tables
Goal: Store users, projects, and project-scoped roles.
Description: Add a database migration and SQLAlchemy models for users, projects, and project memberships. A membership must identify whether the user is a manager or a team member for that specific project.

## 7. Implement local login and session selection
Goal: Let a trusted local user enter the application as a selected user.
Description: Add a simple local login or user-selection flow suitable for the MVP, storing the active user in the Streamlit session. The feature must make it clear that this is not production-grade authentication.

## 8. Create the project-management screen
Goal: Allow a manager to create and configure a project.
Description: Build a manager-only Streamlit screen for creating a project and setting its timezone and retrospective time. Validate the values and save them in PostgreSQL.

## 9. Create member-management controls
Goal: Allow a manager to manage members and their project roles.
Description: Build a manager-only Streamlit screen to add and remove existing users from a project and assign the manager or team-member role. Prevent duplicate memberships and prevent a user without manager permission from changing membership data.

## 10. Create the weekly-cycle data model
Goal: Represent one project's active weekly feedback period.
Description: Add a migration and model for a weekly cycle with its project, start time, closure time, retrospective time, and status. Include helper logic that determines whether the current cycle is open using the project's timezone.

## 11. Build current-cycle creation and display
Goal: Ensure each project has a visible current weekly cycle.
Description: Implement logic that creates or retrieves the current Monday-to-Friday cycle for a selected project. Add a Streamlit view that shows the cycle dates, the Friday 10:00 deadline, and whether feedback is open or closed.

## 12. Create the feedback-submission schema
Goal: Store one structured feedback submission per member per weekly cycle.
Description: Add a migration and model containing weekly update, progress, what worked, blockers, improvements, suggestions, other feedback, author, cycle, and anonymous status. Enforce a database-level rule that a member can have only one submission per cycle.

## 13. Build the team-member feedback form
Goal: Let a team member create or edit their feedback while a cycle is open.
Description: Build a Streamlit form containing every feedback field from the plan and an anonymous-submission option. Load the member's existing submission for editing, and reject create or update attempts after the backend cycle rule reports the cycle as closed.

## 14. Protect anonymous feedback in manager views
Goal: Ensure managers never see an anonymous submission's author in the application.
Description: Create a data-access method for manager feedback views that removes the author identity whenever a submission is marked anonymous. Add automated tests covering attributed and anonymous submissions so the privacy rule is not accidentally removed.

## 15. Build the feedback board
Goal: Give a manager a categorized view of the current cycle's feedback.
Description: Build a manager-only Streamlit board grouped into what worked, blockers, improvements, suggestions, and other feedback. Show author names only for attributed feedback and display an anonymous label for anonymous feedback.

## 16. Create retrospective, decision, and action-item tables
Goal: Store the outcomes of a weekly retrospective.
Description: Add migrations and SQLAlchemy models for a retrospective record, decisions, and action items. An action item must include a description, owner, and deadline and must belong to the relevant weekly cycle.

## 17. Build the retrospective meeting view
Goal: Let a manager record decisions and action items during the retrospective.
Description: Build a manager-only Streamlit page that shows the current feedback board alongside controls for adding, editing, and removing decisions and action items. Validate that action-item owners belong to the selected project and that a deadline is supplied.

## 18. Add in-app reminder messages
Goal: Encourage incomplete feedback without requiring an email service.
Description: Display a reminder to a team member who opens the app on Wednesday, Thursday, or Friday morning without a submission for the current cycle. The reminder is informational only and must not block use of the application.

## 19. Add completed-cycle cleanup
Goal: Remove completed weekly feedback data after its retrospective.
Description: Implement a cleanup function that identifies cycles whose configured retrospective time has passed and deletes their feedback, retrospective, decisions, and action items. Run this function safely when the application starts, and add tests proving it preserves projects, users, and memberships.

## 20. Add end-to-end workflow checks and run documentation
Goal: Verify and document the full local MVP workflow.
Description: Add automated checks for the key rules: project roles, Friday closure, anonymous display, and completed-cycle cleanup. Write concise instructions for starting PostgreSQL and Streamlit with Docker Compose and for running the test suite.
