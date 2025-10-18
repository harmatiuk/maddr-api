from fastapi import FastAPI
from maddr_api.routers import account

app = FastAPI()

app.include_router(account.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the MADDR API!"}
