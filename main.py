from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Pocket Coach API is running!"}

# --- User Profile ---
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
    dietary_preferences: List[str] = []
    allergies: List[str] = []

class MealPlan(BaseModel):
    days: List[Dict]  # e.g., [{"day": "Monday", "meals": [...]}, ...]

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
            {"day": "Tuesday", "meals": [
                {"name": "Greek Yogurt", "calories": 200},
                {"name": "Turkey Sandwich", "calories": 450},
                {"name": "Stir Fry", "calories": 550}
            ]}
        ]
    }

# --- Workout Plan Endpoint ---
class WorkoutPlanRequest(BaseModel):
    user_id: str
    goal: str
    frequency: int
    experience: str

class WorkoutPlan(BaseModel):
    days: List[Dict]  # e.g., [{"day": "Monday", "workout": [...]}, ...]

@app.post("/workoutplan")
def generate_workout_plan(request: WorkoutPlanRequest):
    # Mocked workout plan
    return {
        "days": [
            {"day": "Monday", "workout": [
                {"exercise": "Squat", "sets": 3, "reps": 10},
                {"exercise": "Push-up", "sets": 3, "reps": 15}
            ]},
            {"day": "Tuesday", "workout": [
                {"exercise": "Deadlift", "sets": 3, "reps": 8},
                {"exercise": "Pull-up", "sets": 3, "reps": 8}
            ]}
        ]
    }
