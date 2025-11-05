from fastapi import FastAPI
from maddr_api.routers import account, token, book, author

app = FastAPI()

app.include_router(account.router)
app.include_router(token.router)
app.include_router(book.router)
app.include_router(author.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the MADDR API!"}
