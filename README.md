# Travel Planner API

API for managing travel and location projects, with integration with the Art Institute of Chicago.

# Installation and startup

Clone the repository
```
git clone <your-repo-url>
cd <project-folder>
```

Create a virtual environment and set dependencies
```
poetry install
```

Create .env file
```
API_URL=https://api.artic.edu/api/v1/artworks
DATABASE_URL=sqlite:///./travel_planner.db
DEBUG=True
```

Launch the application
```
uvicorn app.main:app --reload
```

Swagger is available at: http://localhost:8000/docs

# Endpoints
Projects

- POST /projects/ - create a project with places
- GET /projects/ - list of all projects
- GET /projects/{project_id} - get one project
- PUT /projects/{project_id} - update project
- DELETE /projects/{project_id} - delete project (if there are no places visited)

Places
- POST /places/{project_id} - add a place to the project
- PUT /places/{place_id} — update notes or visit status
- GET /places/{place_id} — receive one place

 For a list of all project locations, use project.places from the endpoint /projects/{project_id}

# Docker (untested)

There is a Dockerfile and docker-compose.yml that launch the application and (optionally) Postgres.

Not yet tested on a local machine, use at your own risk.

Launch via docker-compose:
```
docker-compose up --build
```

Stop:
```
docker-compose down
```