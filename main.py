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

@app.post("/user")
def create_user(profile: UserProfile):
    return profile

# --- Meal Plan Endpoint ---
class MealPlanRequest(BaseModel):
    user_id: str
    goal: str
    dietary_preferences: list[str] = []
    allergies: list[str] = []

class MealPlan(BaseModel):
    days: list[dict]  # e.g., [{"day": "Monday", "meals": [...]}, ...]

@app.post("/mealplan")
def generate_meal_plan(request: MealPlanRequest):
    # Mocked meal plan
    return {
        "days": [
            {"day": "Monday", "meals": [
                {"name": "Oatmeal", "calories": 350},
                {"name": "Chicken Salad", "calories": 500},
                {"name": "Grilled Salmon", "calories": 600}
            ]},
            # ...more days
        ]
    }

# --- Workout Plan Endpoint ---
class WorkoutPlanRequest(BaseModel):
    user_id: str
    goal: str
    frequency: int
    experience: str

class WorkoutPlan(BaseModel):
    days: list[dict]  #
