from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import json
import firebase_admin
from firebase_admin import credentials, db
import re

# Load Firebase credentials from environment variables
firebase_key = os.getenv("FIREBASE_PRIVATE_KEY")
firebase_db_url = os.getenv("FIREBASE_DATABASE_URL")

if firebase_key and not firebase_admin._apps:
    try:
        firebase_key_dict = json.loads(firebase_key)
        cred = credentials.Certificate(firebase_key_dict)
        firebase_admin.initialize_app(cred, {'databaseURL': firebase_db_url})
        print("✅ Firebase Initialized Successfully")
    except Exception as e:
        print(f"❌ Firebase Initialization Failed: {e}")

# Function to save calculations to Firebase
def save_to_firebase(first_value, second_value, operation, result):
    try:
        ref = db.reference("calculations")
        new_entry = ref.push()
        new_entry.set({
            "first_value": first_value,
            "second_value": second_value,
            "operation": operation,
            "result": result
        })
        print(f"✅ Data saved to Firebase: {first_value} {operation} {second_value} = {result}")
    except Exception as e:
        print(f"❌ Error saving data to Firebase: {e}")

# HTML frontend
def hello_world(request):
    html = """
    <html lang="en">
    <head><title>Calculator API</title></head>
    <body>
        <h1>Welcome to the Calculator API</h1>
        <p>Use the API endpoint <code>/calculate</code> to perform calculations.</p>
    </body>
    </html>
    """
    return Response(html)

# API to handle calculations
def calculate(request):
    try:
        data = request.json_body
        expression = data.get("expression")

        # Validate and extract numbers & operator using regex
        match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", expression)
        if match:
            first_value, operation, second_value = match.groups()
            result = eval(expression)  # Ensure input safety in real cases
            save_to_firebase(first_value, second_value, operation, result)
            return Response(json.dumps({"result": result}), content_type='application/json')
        else:
            print(f"❌ Invalid expression format: {expression}")
            return Response(json.dumps({"error": "Invalid expression format"}), content_type='application/json', status=400)
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), content_type='application/json', status=400)

# Run the server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(hello_world, route_name='home')
        config.add_route('calculate', '/calculate')
        config.add_view(calculate, route_name='calculate', renderer='json')
        app = config.make_wsgi_app()
    
    server = make_server('0.0.0.0', port, app)
    print(f"🚀 Server running on http://localhost:{port}")
    server.serve_forever()
