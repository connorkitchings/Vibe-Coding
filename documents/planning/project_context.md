Project Context
Instructions: This is a living document that defines the project's technical foundation. It should
be kept up-to-date as the architecture or technology stack evolves. It is the single source of truth
for setup, architecture, and coding standards.

1. Overview
Project Goal: [A one-sentence summary of the project's technical goal, e.g., "A resilient REST API
with a reactive frontend."]

Repository: [Link to the Git repository]

2. Architecture
High-Level Summary
[A brief description of the architecture, e.g., "This project follows a simple client-server model.
The frontend is a single-page application (SPA) built with React that communicates with a
Python/FastAPI backend via a REST API."]

System Diagram
+------------------+           +------------------+           +------------------+
| React Frontend   |   <--->   | FastAPI Backend  |   <--->   | PostgreSQL DB    |
| (Vercel)         |           | (Render)         |           | (Supabase)       |
+------------------+           +------------------+           +------------------+

Folder Structure
/client: Contains the React frontend application.

/server: Contains the FastAPI backend application.

/docs: Contains all Vibe Coding System documentation.

/scripts: Contains automation and utility scripts.

3. Technology Stack
Category

Technology

Version

Notes

Frontend

React

18.x

UI library

Backend

Python

3.11+

Core language

Backend

FastAPI

latest

Web framework

Database

PostgreSQL

15+

Primary data store

Styling

Tailwind CSS

latest

Utility-first CSS framework

Testing

Pytest, Jest

latest

Backend and frontend testing

Deployment

Vercel, Render

N/A

Hosting platforms

4. Setup & Environment
Prerequisites
Node.js v18+

Python 3.11+ & pip

Docker (for local database)

Local Setup Instructions
Clone the repository:

git clone [repository-url]
cd [project-folder]

Set up environment variables:

cp .env.example .env

# Fill in the required values in the .env file

Install backend dependencies:

cd server && pip install -r requirements.txt

Install frontend dependencies:

cd ../client && npm install

Run the application:

# In one terminal, from the /server directory

uvicorn main:app --reload

# In another terminal, from the /client directory

npm run dev

5. Standards & Practices
Version Control
Branching Strategy: All work is done on feature branches (e.g., feature/user-auth,
bugfix/login-error). main is the production branch.

Commit Messages: We follow the Conventional Commits specification.

Coding Standards
Python (Backend): Formatted with black and linted with ruff.

JavaScript (Frontend): Formatted with prettier and linted with eslint.

Enforcement: These standards are enforced via the checklists in [QG:PreCommit].

Testing Strategy
Backend: Unit and integration tests are written with pytest.

Frontend: Component and integration tests are written with Jest and React Testing Library.

Requirement: All new features must include corresponding tests, and code coverage should not
decrease. Test quality is enforced via the [QG:PreMerge] checklist.
