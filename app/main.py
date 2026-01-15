from fastapi import FastAPI
from app.routers.rates import router as rates_router


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(rates_router)
