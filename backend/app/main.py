from fastapi import FastAPI,Depends
from app import models, database, auth
from app.database import engine
from app.auth import get_current_user
from app import tattoo_router, appointments, review_router

# create tables
models.Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(title="QWLA", version="0.1.0")

# include auth router
app.include_router(auth.router)
app.include_router(tattoo_router.router)
app.include_router(appointments.router)
app.include_router(review_router.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, this is a protected route!"}

# @app.post("/create-profile")
# def create_tattoo(current_user: models.User = Depends(auth.require_role("artist"))):
#     return {"message": f"Tattoo created by {current_user.username}"}

