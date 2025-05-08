from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Pocket Coach API is running!"}

class UserProfile(BaseModel):
    name: str
    age: int
    gender: str
    # Add more fields as needed

@app.post("/user")
def create_user(profile: UserProfile):
    # For now, just echo back the data
    return profile
