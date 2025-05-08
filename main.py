import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import openai
import base64

app = FastAPI()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    equipment: List[str] = []
    body_scan: Optional[str] = None

@app.post("/user")
def create_user(profile: UserProfile):
    return profile

@app.get("/user/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id, "mock": True}

# --- Meal Plan (Mock) ---
class MealPlanRequest(BaseModel):
    user_id: str
    goal: str
    dietary_preferences: List[str] = []
    allergies: List[str] = []

@app.post("/mealplan")
def generate_meal_plan(request: MealPlanRequest):
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

# --- Meal Plan (AI) ---
@app.post("/mealplan/ai")
def generate_meal_plan_ai(request: MealPlanRequest):
    prompt = (
        f"Create a 1-day meal plan for someone whose goal is {request.goal}. "
        f"Dietary preferences: {', '.join(request.dietary_preferences) or 'none'}. "
        f"Allergies: {', '.join(request.allergies) or 'none'}. "
        "List meals with names, calories, and a short description."
    )
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        return {"plan": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# --- Workout Plan (Mock) ---
class WorkoutPlanRequest(BaseModel):
    user_id: str
    goal: str
    frequency: int
    experience: str
    split: str
    style: str
    equipment: List[str] = []
    body_scan: Optional[str] = None

@app.post("/workoutplan")
def generate_workout_plan(request: WorkoutPlanRequest):
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
    return entry

@app.get("/progress/weight/{user_id}")
def get_weight_history(user_id: str):
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
    return entry

@app.get("/progress/measurements/{user_id}")
def get_measurement_history(user_id: str):
    return [
        {"date": "2024-05-01", "waist": 32, "chest": 40},
        {"date": "2024-05-02", "waist": 31.8, "chest": 40.2}
    ]

# --- Progress Photos ---
@app.post("/progress/photo")
async def upload_progress_photo(user_id: str, file: UploadFile = File(...)):
    return {"filename": file.filename, "user_id": user_id}

@app.get("/progress/photos/{user_id}")
def get_progress_photos(user_id: str):
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
    return {"message": "At this rate, you'll hit your goal in 6 weeks."}

@app.post("/analyze/photos")
async def analyze_photos(front: UploadFile = File(...), back: UploadFile = File(...)):
    front_bytes = await front.read()
    back_bytes = await back.read()
    prompt = (
        "You are a brutally honest fitness coach. Given these front and back body photos, estimate the person's body fat percentage, list their strong and weak points, and give direct, no-nonsense feedback. Do not sugarcoat. Be specific and realistic."
    )
    # Encode images as base64 data URLs
    front_b64 = base64.b64encode(front_bytes).decode()
    back_b64 = base64.b64encode(back_bytes).decode()
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{front_b64}"}},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{back_b64}"}}
        ]}
    ]
    response = openai_client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=500,
    )
    critique = response.choices[0].message.content
    return {"critique": critique} 
