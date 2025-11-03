from fastapi import FastAPI
from maddr_api.routers import account, token, book, novelist

app = FastAPI()

app.include_router(account.router)
app.include_router(token.router)
app.include_router(book.router)
app.include_router(novelist.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MADDR API!"}
