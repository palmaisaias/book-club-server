from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.routers.monthly import router as monthly_router
from app.routers.auth import router as auth_router, get_current_user
from app.routers.suggestions import router as suggestions_router

app = FastAPI(title="Sibling Book‑Club API")

# allow the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(auth_router)
app.include_router(suggestions_router, dependencies=[Depends(get_current_user)])
app.include_router(monthly_router, dependencies=[Depends(get_current_user)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)