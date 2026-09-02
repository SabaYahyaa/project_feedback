# Backlog

## 1. Create the Django project and passing test
Goal: Establish a runnable Django project with one automated test that passes.
Description: Create the initial Django project structure, dependency definition, and pytest configuration. Add one minimal test that can run locally and passes, without implementing product functionality. Define these required Python packages in the dependency file: `Django`, `psycopg[binary]`, `django-environ`, `pytest`, `pytest-django`, `langchain`, `langchain-ollama`, and `pydantic`. Pin compatible versions after the initial environment is created. Do not add an external LLM SDK: the application will call the locally running Ollama service.

## 2. Define Django environment configuration
Goal: Define the non-secret settings and secrets required by the Django application.
Description: Configure Django to read its secret key, debug setting, allowed hosts, and PostgreSQL connection details from environment variables. Provide a safe example environment file and ensure real local secrets are excluded from Git.

## 3. Add Docker Compose services
Goal: Run Django and PostgreSQL together through Docker Compose.
Description: Define a Compose setup with a Django service and a PostgreSQL 17 service using the `pgvector/pgvector:pg17` image. Configure service networking, persistent PostgreSQL storage, environment variables, and local ports without committing credentials.

## 4. Connect Django to PostgreSQL
Goal: Configure Django to use PostgreSQL instead of its default database.
Description: Use the `psycopg` PostgreSQL driver and Django settings to connect to the Docker PostgreSQL service. Add a small test or documented check that clearly reports when the database is unavailable.

## 5. Configure Django migrations and admin access
Goal: Create the Django database tables and enable the built-in administration site.
Description: Apply Django's initial migrations to PostgreSQL and create a local superuser for development. Confirm that the Django admin login can manage built-in user accounts.

## 6. Create the project and membership models
Goal: Store projects and each user's role within a project.
Description: Add Django models and migrations for a project and its memberships, using Django's built-in User model. A membership must identify whether a user is a manager or team member for that specific project.

## 7. Register project data in Django admin
Goal: Let a manager or developer manage projects and memberships through Django admin.
Description: Register the project and membership models in Django admin with useful list columns and search fields. Make it practical to create a manager user and a few team-member test users without writing database commands.

## 8. Add login, logout, and protected pages
Goal: Require a logged-in Django user before accessing application pages.
Description: Add Django login and logout views and a base page layout showing the signed-in user. Protect project pages so an unauthenticated visitor is redirected to the login page.

## 9. Add project membership authorization helpers
Goal: Enforce project access and manager-only permissions consistently.
Description: Create reusable Django helpers or mixins that confirm the logged-in user belongs to the selected project and has the required role. Add tests showing that non-members and team members cannot access manager-only actions.

## 10. Build the project dashboard and setup form
Goal: Allow a manager to create and configure a project.
Description: Create a manager-only Django form and page for the project name, timezone, and retrospective time. Add a project dashboard that shows the selected project and role-appropriate navigation.

## 11. Build member-management pages
Goal: Allow a manager to manage project members and their roles.
Description: Create manager-only Django pages to add and remove existing users from a project and assign the manager or team-member role. Validate duplicate memberships and prevent removal or modification by users without manager permission.

## 12. Create the weekly-cycle model
Goal: Represent one project's Monday-to-Friday feedback period.
Description: Add a Django model and migration for a weekly cycle with its project, start time, closure time, retrospective time, and status. Add model or service helpers that determine whether the cycle is open using the project's timezone.

## 13. Build current-cycle creation and display
Goal: Ensure a selected project has a visible current weekly cycle.
Description: Implement logic that creates or retrieves the current Monday-to-Friday cycle for a project. Display the cycle dates, Friday 10:00 deadline, and open or closed state on the project dashboard.

## 14. Create the feedback-submission model
Goal: Store one structured feedback submission per member per weekly cycle.
Description: Add a Django model and migration containing weekly update, progress, what worked, blockers, improvements, suggestions, other feedback, author, cycle, and anonymous status. Enforce that a member can have only one submission per cycle.

## 15. Build the team-member feedback form
Goal: Let a team member create or edit feedback while the cycle is open.
Description: Create a Django form and page containing every feedback field from the plan and an anonymous-submission option. Load the member's existing submission for editing and reject create or update requests when the cycle is closed.

## 16. Protect anonymous feedback in manager views
Goal: Ensure managers never see an anonymous submission's author in the application.
Description: Create manager-facing query and template logic that hides author identity whenever a submission is marked anonymous. Add automated tests covering attributed and anonymous submissions so the privacy rule cannot be accidentally removed.

## 17. Build the feedback board
Goal: Give a manager a categorized view of the current cycle's feedback.
Description: Create a manager-only Django page that groups feedback into what worked, blockers, improvements, suggestions, and other feedback. Show author names only for attributed feedback and an anonymous label for anonymous feedback.

## 18. Create retrospective, decision, and action-item models
Goal: Store the outcomes of a weekly retrospective.
Description: Add Django models and migrations for a retrospective record, decisions, and action items. An action item must include a description, owner, and deadline and must belong to the relevant weekly cycle.

## 19. Build the retrospective page
Goal: Let a manager record decisions and action items during the retrospective.
Description: Create a manager-only Django page that shows the feedback board alongside forms for adding, editing, and removing decisions and action items. Validate that each action-item owner belongs to the selected project and that a deadline is supplied.

## 20. Add in-app reminder messages
Goal: Encourage incomplete feedback without requiring an email service.
Description: Display a Django message to a member who visits the app on Wednesday, Thursday, or Friday morning without a submission for the current cycle. The reminder is informational only and must not block use of the application.

## 21. Add completed-cycle cleanup
Goal: Remove completed weekly feedback data after its retrospective.
Description: Implement a cleanup service that identifies cycles whose configured retrospective time has passed and deletes their feedback, retrospective, decisions, and action items. Run it safely when the application receives a request and add tests proving it preserves projects, users, and memberships.

## 22. Add end-to-end workflow checks and run documentation
Goal: Verify and document the full local MVP workflow.
Description: Add automated checks for project roles, Friday closure, anonymous display, and completed-cycle cleanup. Write concise instructions for starting Django and PostgreSQL with Docker Compose, creating test users through Django admin, and running the test suite.

## 23. Add local LLM feedback analysis
Goal: Generate a manager-facing summary of a weekly cycle's feedback using a local Ollama model.
Description: Configure LangChain's `ChatOllama` integration to use `gemma3:4b`, with the Ollama base URL and model name supplied through environment variables. Add a service that sends only the selected cycle's feedback to the model and returns a structured summary of themes, blockers, improvements, and suggested discussion points. Preserve anonymous submissions by excluding author identity from the prompt whenever a submission is anonymous. Add tests that mock the LLM client, so the test suite does not require Ollama or a downloaded model. Document the local prerequisite: install Ollama and run `ollama pull gemma3:4b`.

## Optional packages for a later retrieval feature
Use these only if we decide to search across historical feedback or uploaded documents: `pgvector`, `langchain-text-splitters`, and an Ollama embedding model such as `nomic-embed-text`. They are not required for the weekly-summary feature above.
