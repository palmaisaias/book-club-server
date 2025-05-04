import random
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from app.schemas import MonthlyPickOut

router = APIRouter(prefix="/monthly", tags=["monthly"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pick", response_model=MonthlyPickOut)
def create_monthly_pick(db: Session = Depends(get_db)):
    # e.g. "2025-05"
    month_str = datetime.date.today().strftime("%Y-%m")
    # if we’ve already picked this month, return it
    existing = db.query(models.MonthlyPick).filter_by(month=month_str).first()
    if existing:
        return existing

    choices = db.query(models.Suggestion).all()
    if not choices:
        raise HTTPException(status_code=404, detail="No suggestions available")

    pick = models.MonthlyPick(
        suggestion_id=random.choice(choices).id,
        month=month_str
    )
    db.add(pick)
    db.commit()
    db.refresh(pick)
    return pick

@router.get("/pick", response_model=MonthlyPickOut)
def get_monthly_pick(db: Session = Depends(get_db)):
    month_str = datetime.date.today().strftime("%Y-%m")
    pick = db.query(models.MonthlyPick).filter_by(month=month_str).first()
    if not pick:
        raise HTTPException(status_code=404, detail="No pick set for this month")
    return pick