import copy

import pytest
from fastapi.testclient import TestClient

import main
from data import movies

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_db():
    """Restore the in-memory store before each test so tests don't affect each other."""
    main.db[:] = copy.deepcopy(movies)


# ---------- GET /movies ----------

def test_list_all_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) == len(movies)


def test_filter_by_genre_is_case_insensitive():
    response = client.get("/movies", params={"genre": "Sci-Fi"})
    assert response.status_code == 200
    assert {m["id"] for m in response.json()} == {1, 3, 5, 10}


def test_filter_by_min_rating():
    response = client.get("/movies", params={"min_rating": 8.8})
    assert {m["id"] for m in response.json()} == {1, 2, 6, 8}


def test_filter_by_year():
    response = client.get("/movies", params={"year": 2010})
    assert [m["title"] for m in response.json()] == ["Inception"]


def test_combined_filters():
    response = client.get("/movies", params={"genre": "sci-fi", "min_rating": 8.7})
    assert {m["id"] for m in response.json()} == {1, 5}


def test_invalid_min_rating_returns_422():
    response = client.get("/movies", params={"min_rating": 11})
    assert response.status_code == 422


# ---------- GET /movies/{id} ----------

def test_get_movie_by_id():
    response = client.get("/movies/8")
    assert response.status_code == 200
    assert response.json()["title"] == "The Godfather"


def test_get_missing_movie_returns_404():
    response = client.get("/movies/999")
    assert response.status_code == 404


# ---------- POST /movies ----------

def test_create_movie():
    payload = {"title": "Dune", "genre": "sci-fi", "rating": 8.0, "year": 2021}
    response = client.post("/movies", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 11
    assert body["title"] == "Dune"
    assert client.get("/movies/11").status_code == 200


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "Bad", "genre": "drama", "rating": 15, "year": 2020},   # rating > 10
        {"title": "Bad", "genre": "drama", "rating": 5, "year": 1500},    # year too early
        {"title": "", "genre": "drama", "rating": 5, "year": 2020},       # empty title
        {"genre": "drama", "rating": 5, "year": 2020},                    # missing title
    ],
)
def test_create_movie_with_invalid_data_returns_422(payload):
    response = client.post("/movies", json=payload)
    assert response.status_code == 422


# ---------- PUT /movies/{id} ----------

def test_update_movie_changes_only_sent_fields():
    response = client.put("/movies/1", json={"rating": 9.1})
    assert response.status_code == 200
    body = response.json()
    assert body["rating"] == 9.1
    assert body["title"] == "Inception"


def test_update_missing_movie_returns_404():
    response = client.put("/movies/999", json={"rating": 5})
    assert response.status_code == 404


# ---------- DELETE /movies/{id} ----------

def test_delete_movie():
    response = client.delete("/movies/1")
    assert response.status_code == 204
    assert client.get("/movies/1").status_code == 404


def test_delete_missing_movie_returns_404():
    response = client.delete("/movies/999")
    assert response.status_code == 404


# ---------- GET /movies/{id}/recommendations ----------

def test_recommendations_are_same_genre_sorted_by_rating():
    response = client.get("/movies/1/recommendations")
    assert response.status_code == 200
    assert [m["id"] for m in response.json()] == [5, 3, 10]


def test_recommendations_respect_limit():
    response = client.get("/movies/1/recommendations", params={"limit": 2})
    assert [m["id"] for m in response.json()] == [5, 3]


def test_recommendations_exclude_the_movie_itself():
    response = client.get("/movies/1/recommendations", params={"limit": 10})
    assert 1 not in [m["id"] for m in response.json()]


def test_recommendations_for_missing_movie_returns_404():
    response = client.get("/movies/999/recommendations")
    assert response.status_code == 404
