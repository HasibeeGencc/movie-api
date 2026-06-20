from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from models import Movie, MovieCreate, MovieUpdate
from data import movies
import copy

app = FastAPI(
    title="Movie Recommendation API",
    description="A simple REST API to manage and filter movies.",
    version="1.0.0"
)

db = copy.deepcopy(movies)


def get_next_id() -> int:
    return max(m["id"] for m in db) + 1 if db else 1


@app.get("/movies", response_model=list[Movie], tags=["Movies"])
def get_movies(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    min_rating: Optional[float] = Query(None, ge=0, le=10, description="Minimum rating"),
    year: Optional[int] = Query(None, description="Filter by release year"),
):
    result = db
    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]
    if min_rating is not None:
        result = [m for m in result if m["rating"] >= min_rating]
    if year:
        result = [m for m in result if m["year"] == year]
    return result


@app.get("/movies/{movie_id}", response_model=Movie, tags=["Movies"])
def get_movie(movie_id: int):
    movie = next((m for m in db if m["id"] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies", response_model=Movie, status_code=201, tags=["Movies"])
def create_movie(movie: MovieCreate):
    new_movie = {"id": get_next_id(), **movie.model_dump()}
    db.append(new_movie)
    return new_movie


@app.put("/movies/{movie_id}", response_model=Movie, tags=["Movies"])
def update_movie(movie_id: int, updates: MovieUpdate):
    movie = next((m for m in db if m["id"] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        movie[field] = value
    return movie


@app.delete("/movies/{movie_id}", status_code=204, tags=["Movies"])
def delete_movie(movie_id: int):
    movie = next((m for m in db if m["id"] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.remove(movie)
    return None


@app.get("/movies/{movie_id}/recommendations", response_model=list[Movie], tags=["Recommendations"])
def get_recommendations(movie_id: int, limit: int = Query(3, ge=1, le=10)):
    movie = next((m for m in db if m["id"] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    similar = [
        m for m in db
        if m["genre"] == movie["genre"] and m["id"] != movie_id
    ]
    similar.sort(key=lambda x: x["rating"], reverse=True)
    return similar[:limit]
