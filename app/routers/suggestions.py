import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_suggestion(username: str, title: str, author: str | None = "", db: Session = Depends(get_db)):
    suggestion = models.Suggestion(username=username, title=title, author=author)
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion


@router.get("/user/{username}")
def user_suggestions(username: str, db: Session = Depends(get_db)):
    return db.query(models.Suggestion).filter(models.Suggestion.username == username).all()


@router.get("/current-book")
def current_book(db: Session = Depends(get_db)):
    all_suggestions = db.query(models.Suggestion).all()
    if not all_suggestions:
        raise HTTPException(status_code=404, detail="No suggestions found")
    return random.choice(all_suggestions)