# server/app/routers/admin.py

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, Base
from app.routers.auth import get_current_user  # assuming you have this
from app.db import models

router = APIRouter(prefix="/admin", tags=["admin"])

# Local get_db (database.py exports SessionLocal, not get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete(
    "/clear-all",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)]
)
def clear_all_data(db: Session = Depends(get_db)):
    """
    Delete ALL rows from ALL tables (in reverse metadata order).
    WARNING: irreversible!
    """
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)