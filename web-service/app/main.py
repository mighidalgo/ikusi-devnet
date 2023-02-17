from fastapi import FastAPI
from .routers import fetch

app = FastAPI()
app.include_router(fetch.router)

@app.get("/")
async def root():
	return {"Hello":"World!"}