import random
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import models
from app.schemas import SuggestionCreate, SuggestionOut

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=SuggestionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_suggestion(
    payload: SuggestionCreate,
    db: Session = Depends(get_db),
):
    """
    Expects a JSON body:
    {
      "username": "user1",
      "title": "My Book Title",
      "author": "Author Name"
    }
    """
    # Debug log
    print(f"[create_suggestion] payload: {payload.dict()}")

    suggestion = models.Suggestion(
        username=payload.username,
        title=payload.title,
        author=payload.author or "",
    )
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)

    # Debug log
    print(f"[create_suggestion] created suggestion id={suggestion.id}")

    return suggestion


@router.get(
    "/user/{username}",
    response_model=list[SuggestionOut],
)
def user_suggestions(
    username: str,
    db: Session = Depends(get_db),
):
    print(f"[user_suggestions] Fetching for user: {username}")
    result = db.query(models.Suggestion).filter(models.Suggestion.username == username).all()
    print(f"[user_suggestions] Found {len(result)} items")
    return result


@router.get("/current-book")
def current_book(db: Session = Depends(get_db)):
    print("[current_book] Selecting random book")
    all_suggestions = db.query(models.Suggestion).all()
    if not all_suggestions:
        print("[current_book] No suggestions found")
        raise HTTPException(status_code=404, detail="No suggestions found")
    book = random.choice(all_suggestions)
    print(f"[current_book] Selected id={book.id} title={book.title}")
    return book


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_suggestions(db: Session = Depends(get_db)):
    print("[clear_suggestions] Clearing suggestions and picks")
    db.query(models.Suggestion).delete()
    db.query(models.MonthlyPick).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)