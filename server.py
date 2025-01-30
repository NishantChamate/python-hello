import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from pyramid.config import Configurator
from pyramid.response import Response
from waitress import serve  # Better for production WSGI

# Load Firebase credentials from environment variable
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials:
    try:
        cred_dict = json.loads(firebase_credentials)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully")
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")
        raise
else:
    print("❌ Firebase credentials not found in environment variables")
    raise ValueError("Firebase credentials not found in environment variables")

# Health check endpoint
def health_check(request):
    return Response("OK", content_type="text/plain", status=200)

def home_page(request):
    return Response("App is running", content_type="text/plain", status=200)

def calculate_and_store(request):
    try:
        num1 = int(request.GET.get('num1', 0))
        num2 = int(request.GET.get('num2', 0))
        
        results = {
            "Number 1": num1,
            "Number 2": num2,
            "Addition": num1 + num2,
            "Subtraction": num1 - num2,
            "Multiplication": num1 * num2,
            "Division": num1 / num2 if num2 != 0 else "undefined",
            "Modulus": num1 % num2 if num2 != 0 else "undefined",
            "Exponentiation": num1 ** num2,
            "Floor Division": num1 // num2 if num2 != 0 else "undefined"
        }
        
        print("✅ Storing data in Firebase:", results)
        db.collection("calculations").add(results)

        return Response(json.dumps(results, indent=4), content_type="application/json", status=200)

    except Exception as e:
        print(f"❌ Error in calculation: {e}")
        return Response(json.dumps({"error": str(e)}), content_type="application/json", status=500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Default to 8080
    with Configurator() as config:
        config.add_route('health', '/health')  # Explicit health check
        config.add_view(health_check, route_name='health')

        config.add_route('home', '/')
        config.add_view(home_page, route_name='home')

        config.add_route('calculate', '/calculate')
        config.add_view(calculate_and_store, route_name='calculate', renderer="json")

        app = config.make_wsgi_app()
    
    print(f"🚀 Server running on port {port}")
    serve(app, host="0.0.0.0", port=port)  # Use Waitress for production stability
