from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db, Base, engine
from app.core.security import get_current_user, is_admin  # if you have roles

router = APIRouter(prefix="/admin", tags=["admin"])

@router.delete(
    "/clear-all",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user), Depends(is_admin)]
)
def clear_all_data(db: Session = Depends(get_db)):
    """
    Delete ALL rows from ALL tables.
    WARNING: irreversible!
    """
    # Option A: iterate through ORM tables
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()

    # Option B (Postgres-only): 
    # db.execute("TRUNCATE suggestions, monthly_picks, users RESTART IDENTITY CASCADE;")
    # db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)