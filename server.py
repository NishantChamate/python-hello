from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Initialize FastAPI app
app = FastAPI()

# Load Firebase credentials from environment variables
firebase_key = os.getenv("FIREBASE_PRIVATE_KEY")
firebase_db_url = os.getenv("FIREBASE_DATABASE_URL")

# Initialize Firebase
if firebase_key and not firebase_admin._apps:
    try:
        firebase_key_dict = json.loads(firebase_key)
        cred = credentials.Certificate(firebase_key_dict)
        firebase_admin.initialize_app(cred, {'databaseURL': firebase_db_url})
        print("✅ Firebase Initialized Successfully")
    except Exception as e:
        print(f"❌ Firebase Initialization Failed: {e}")

# Define request model
class CalculationRequest(BaseModel):
    input1: float
    input2: float
    operation: str

# Function to perform calculation
def perform_calculation(input1, input2, operation):
    if operation == "+":
        return input1 + input2
    elif operation == "-":
        return input1 - input2
    elif operation == "*":
        return input1 * input2
    elif operation == "/":
        if input2 == 0:
            raise ValueError("Division by zero is not allowed")
        return input1 / input2
    else:
        raise ValueError("Invalid operation. Supported: +, -, *, /")

# Function to store result in Firebase
def save_to_firebase(input1, input2, operation, result):
    try:
        ref = db.reference("calculations")

        # Get count of previous calculations to generate unique IDs
        calculations = ref.get()
        next_id = len(calculations) + 1 if calculations else 1

        # Store calculation
        ref.child(f"calculation_{next_id}").set({
            "input1": input1,
            "input2": input2,
            "operation": operation,
            "result": result
        })

        print(f"✅ Calculation saved to Firebase: calculation_{next_id}")

    except Exception as e:
        print(f"❌ Error saving to Firebase: {e}")

# API Endpoint for calculations
@app.post("/calculate")
def calculate(request: CalculationRequest):
    try:
        result = perform_calculation(request.input1, request.input2, request.operation)
        save_to_firebase(request.input1, request.input2, request.operation, result)
        return {"input1": request.input1, "input2": request.input2, "operation": request.operation, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run with: uvicorn filename:app --host 0.0.0.0 --port 8080
