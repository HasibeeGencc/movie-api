from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: int
    title: str
    genre: str
    rating: float
    year: int

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    genre: str = Field(..., min_length=1)
    rating: float = Field(..., ge=0.0, le=10.0)
    year: int = Field(..., ge=1888, le=2100)

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    year: Optional[int] = Field(None, ge=1888, le=2100)
