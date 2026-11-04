# 🎬 Movie Recommendation API

A RESTful API built with **FastAPI** for managing a movie catalogue and getting simple, genre-based recommendations. It supports full CRUD, query filtering, request validation with **Pydantic v2**, and auto-generated interactive docs via **Swagger/OpenAPI**.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
[![Tests](https://github.com/HasibeeGencc/movie-api/actions/workflows/tests.yml/badge.svg)](https://github.com/HasibeeGencc/movie-api/actions/workflows/tests.yml)

<!-- Add a screenshot of the Swagger UI at docs/swagger.png, then uncomment:
![Swagger UI](docs/swagger.png)
-->

---

## Features

- **CRUD endpoints** for movies (create, read, update, delete)
- **Filtering** by genre (case-insensitive), minimum rating and release year
- **Recommendations**: returns the highest-rated movies in the same genre as a given movie
- **Validation** with Pydantic: ratings must be 0–10, years 1888–2100, titles 1–100 characters; invalid input returns `422`
- **Proper HTTP semantics**: `201 Created`, `204 No Content`, `404 Not Found`
- **Interactive API docs** generated automatically at `/docs` (Swagger UI) and `/redoc`
- **Automated tests** with pytest, run on every push via GitHub Actions
- **Dockerfile** for running the API in a container

## Tech Stack

| Area | Tools |
|------|-------|
| Language | Python 3.12 |
| Framework | FastAPI, Uvicorn |
| Validation | Pydantic v2 |
| Testing | pytest, FastAPI TestClient |
| DevOps | Docker, GitHub Actions |

## Project Structure

```
movie-api/
├── main.py              # FastAPI app and route handlers
├── models.py            # Pydantic request/response models
├── data.py              # Seed data (10 movies)
├── tests/
│   └── test_main.py     # API tests
├── requirements.txt     # Runtime dependencies
├── requirements-dev.txt # Test dependencies
├── Dockerfile
└── .github/workflows/tests.yml
```

## Getting Started

### Run locally

```bash
git clone https://github.com/HasibeeGencc/movie-api.git
cd movie-api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000/docs** to explore and try every endpoint in the browser.

### Run with Docker

```bash
docker build -t movie-api .
docker run -p 8000:8000 movie-api
```

### Run the tests

```bash
pip install -r requirements-dev.txt
pytest
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/movies` | List movies. Optional filters: `genre`, `min_rating`, `year` |
| `GET` | `/movies/{id}` | Get a single movie |
| `POST` | `/movies` | Create a movie |
| `PUT` | `/movies/{id}` | Update one or more fields of a movie |
| `DELETE` | `/movies/{id}` | Delete a movie |
| `GET` | `/movies/{id}/recommendations` | Top-rated movies in the same genre. Optional `limit` (1–10, default 3) |

### Examples

**Filter sci-fi movies rated 8.7 or higher**

```bash
curl "http://127.0.0.1:8000/movies?genre=sci-fi&min_rating=8.7"
```

```json
[
  {"id": 1, "title": "Inception", "genre": "sci-fi", "rating": 8.8, "year": 2010},
  {"id": 5, "title": "The Matrix", "genre": "sci-fi", "rating": 8.7, "year": 1999}
]
```

**Get recommendations for _Inception_**

```bash
curl "http://127.0.0.1:8000/movies/1/recommendations?limit=2"
```

```json
[
  {"id": 5, "title": "The Matrix", "genre": "sci-fi", "rating": 8.7, "year": 1999},
  {"id": 3, "title": "Interstellar", "genre": "sci-fi", "rating": 8.6, "year": 2014}
]
```

**Create a movie**

```bash
curl -X POST "http://127.0.0.1:8000/movies" \
  -H "Content-Type: application/json" \
  -d '{"title": "Dune", "genre": "sci-fi", "rating": 8.0, "year": 2021}'
```

**Invalid input is rejected**

```bash
curl -X POST "http://127.0.0.1:8000/movies" \
  -H "Content-Type: application/json" \
  -d '{"title": "Bad Movie", "genre": "drama", "rating": 15, "year": 2020}'
# → 422 Unprocessable Entity: rating must be less than or equal to 10
```

## Design Notes

- **Storage is in-memory.** The API starts from the seed data in `data.py`, and changes are lost when the server restarts. This keeps the project focused on API design; a database is the next step (see roadmap).
- **Recommendations are rule-based**: same genre, sorted by rating. It's intentionally simple and easy to swap for a smarter approach later.
- `PUT` applies partial updates: only the fields you send are changed.

## Roadmap

- [ ] Persist data in SQLite/PostgreSQL with SQLAlchemy
- [ ] Content-based recommendations (e.g. TF-IDF on descriptions, or embeddings)
- [ ] Pagination for `GET /movies`
- [ ] Deploy a public demo

## Author

**Hasibe Genc** · [LinkedIn](https://www.linkedin.com/in/hasibe-genc-b4b127283/) · [GitHub](https://github.com/HasibeeGencc)
