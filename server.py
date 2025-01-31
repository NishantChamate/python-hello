from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import json
import firebase_admin
from firebase_admin import credentials, db
import re

# Load Firebase credentials from GitHub Actions secret
firebase_key = os.getenv("FIREBASE_PRIVATE_KEY")
firebase_db_url = os.getenv("FIREBASE_DATABASE_URL")


if firebase_key and not firebase_admin._apps:
    try:
        firebase_key_dict = json.loads(firebase_key)
        cred = credentials.Certificate(firebase_key_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': firebase_db_url
        })
        print("✅ Firebase Initialized Successfully")
    except Exception as e:
        print(f"❌ Firebase Initialization Failed: {e}")
# Initialize Firebase
try:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_FILE)
    firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})
    print("✅ Firebase initialized successfully.")
except Exception as e:
    print(f"❌ Firebase initialization error: {e}")

# Function to save calculations to Firebase
def save_to_firebase(first_value, second_value, operation, result):
    try:
        ref = db.reference("calculations")
        ref.push({
        new_entry = ref.push()
        new_entry.set({
            "first_value": first_value,
            "second_value": second_value,
            "operation": operation,
            "result": result
        })
        print("✅ Data saved to Firebase:", first_value, operation, second_value, "=", result)
        print(f"✅ Data pushed to Firebase: {first_value} {operation} {second_value} = {result}")
    except Exception as e:
        print(f"❌ Error saving data to Firebase: {e}")
        print(f"❌ Firebase push error: {e}")

# HTML frontend
def hello_world(request):
    html = """
    <html lang="en">
@@ -100,25 +98,21 @@ def hello_world(request):
    """
    return Response(html)

# API to handle calculations
def calculate(request):
    try:
        data = request.json_body
        expression = data.get("expression")
        result = eval(expression)
        # Extract operands and operator using regex
        match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", expression)
        if match:
            first_value, operation, second_value = match.groups()
        operands = expression.split(" ")
        if len(operands) == 3:
            first_value, operation, second_value = operands
            save_to_firebase(first_value, second_value, operation, result)
        else:
            print("❌ Invalid expression format:", expression)
            return Response(json.dumps({"error": "Invalid expression format"}), content_type='application/json', status=400)
        return Response(json.dumps({"result": result}), content_type='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), content_type='application/json', status=400)

# Run the server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  
    with Configurator() as config:
@@ -128,5 +122,5 @@ def calculate(request):
        config.add_view(calculate, route_name='calculate', renderer='json')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    print(f"🚀 Server running on port {port}")
    print(f"🚀 Server running on http://localhost:{port}")
    server.serve_forever()
