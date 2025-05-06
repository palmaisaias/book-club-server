from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.routers.monthly import router as monthly_router
from app.routers.auth import router as auth_router, get_current_user
from app.routers.suggestions import router as suggestions_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.routers.monthly import create_monthly_pick
from app.db.database import SessionLocal
from app.routers.admin import router as admin_router



app = FastAPI(title="Sibling Book‑Club API")

# Allowed CORS origins
origins = [
    "http://localhost:5173",                   # Vite dev server
    "https://book-club-client.vercel.app",     # Deployed front end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(auth_router)
app.include_router(suggestions_router, dependencies=[Depends(get_current_user)])
app.include_router(monthly_router, dependencies=[Depends(get_current_user)])
app.include_router(admin_router, dependencies=[Depends(get_current_user)])

@app.on_event("startup")
async def start_scheduler():
    scheduler = AsyncIOScheduler()

    def run_monthly():
        db = SessionLocal()
        try:
            # create or re-create this month's pick
            create_monthly_pick(db=db)
        finally:
            db.close()

    # Schedule to run at 00:00 UTC on the 1st of every month
    scheduler.add_job(run_monthly, trigger="cron", day="1", hour="0", minute="0")
    scheduler.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)