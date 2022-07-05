from fastapi import FastAPI
import rpyc

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to gateway service"}


@app.get("/docs")
async def docs():
    return {"message": "Hello World"}
