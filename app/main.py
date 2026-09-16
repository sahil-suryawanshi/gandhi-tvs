from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Gandhi TVS API is working"}