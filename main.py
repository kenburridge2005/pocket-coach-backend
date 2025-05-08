from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Pocket Coach API is running!"}

# --- User Profile ---
class UserProfile(BaseModel):
    user_id: str
    name: str
    age: int
    gender: str
    height: float
    weight: float
    goal: str
    activity_level: str
    dietary_preferences: List[str] = []
    allergies: List[str] = []
    meal_frequency: str
    experience: str
    split: str
    style: str
    equipment: str
    body_scan: Optional[str] = None

@app.post("/user")
def create_user(profile: UserProfile):
    # In production, save to DB
    return profile

@app.get("/user/{user_id}")
def get_user(user_id: str):
    # In production, fetch from DB
    return {"user_id": user_id, "mock": True}

# --- Meal Plan ---
class MealPlanRequest(BaseModel):
    user_id: str
    goal: str
    dietary_preferences: List[str] = []
    allergies: List[str] = []

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

# --- Workout Plan ---
class WorkoutPlanRequest(BaseModel):
    user_id: str
    goal: str
    frequency: int
    experience: str
    split: str
    style: str
    equipment: str
    body_scan: Optional[str] = None

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

# --- Weight/Progress Tracking ---
class WeightEntry(BaseModel):
    user_id: str
    date: date
    weight: float

@app.post("/progress/weight")
def log_weight(entry: WeightEntry):
    # In production, save to DB
    return entry

@app.get("/progress/weight/{user_id}")
def get_weight_history(user_id: str):
    # In production, fetch from DB
    return [
        {"date": "2024-05-01", "weight": 180},
        {"date": "2024-05-02", "weight": 179.5},
        {"date": "2024-05-03", "weight": 179}
    ]

# --- Measurement Tracking ---
class MeasurementEntry(BaseModel):
    user_id: str
    date: date
    waist: Optional[float] = None
    chest: Optional[float] = None
    hips: Optional[float] = None
    arms: Optional[float] = None
    legs: Optional[float] = None

@app.post("/progress/measurements")
def log_measurements(entry: MeasurementEntry):
    # In production, save to DB
    return entry

@app.get("/progress/measurements/{user_id}")
def get_measurement_history(user_id: str):
    # In production, fetch from DB
    return [
        {"date": "2024-05-01", "waist": 32, "chest": 40},
        {"date": "2024-05-02", "waist": 31.8, "chest": 40.2}
    ]

# --- Progress Photos ---
@app.post("/progress/photo")
async def upload_progress_photo(user_id: str, file: UploadFile = File(...)):
    # In production, save file and link to user
    return {"filename": file.filename, "user_id": user_id}

@app.get("/progress/photos/{user_id}")
def get_progress_photos(user_id: str):
    # In production, fetch from DB
    return [
        {"date": "2024-05-01", "url": "https://example.com/photo1.jpg"},
        {"date": "2024-05-08", "url": "https://example.com/photo2.jpg"}
    ]

# --- Stubs for AI/Feedback/Advanced Features ---
@app.get("/ai/feedback/{user_id}")
def get_ai_feedback(user_id: str):
    return {"message": "Great consistency! Increasing upper body volume next week."}

@app.get("/ai/prediction/{user_id}")
def get_progress_prediction(user_id: str):
    return {"message": "At this rate, you’ll hit your goal in 6 weeks."}
    import os
import openai
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

# ... (your other endpoints and models)

class MealPlanRequest(BaseModel):
    user_id: str
    goal: str
    dietary_preferences: List[str] = []
    allergies: List[str] = []

@app.post("/mealplan/ai")
def generate_meal_plan_ai(request: MealPlanRequest):
    prompt = (
        f"Create a 1-day meal plan for someone whose goal is {request.goal}. "
        f"Dietary preferences: {', '.join(request.dietary_preferences) or 'none'}. "
        f"Allergies: {', '.join(request.allergies) or 'none'}. "
        "List meals with names, calories, and a short description."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    return {"plan": response.choices[0].message["content"]}

# You can do the same for /workoutplan/ai
