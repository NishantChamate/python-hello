import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

# Load Firebase credentials from environment variable
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials:
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    raise ValueError("Firebase credentials not found in environment variables")

def calculate_and_store(request):
    try:
        num1 = int(request.GET.get('num1', 0))
        num2 = int(request.GET.get('num2', 0))

        # Perform calculations
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

        # Store results in Firebase Firestore
        db.collection("calculations").add(results)

        # Return formatted response
        response_html = f"""
        <html>
        <head><title>Calculation Results</title></head>
        <body>
            <h2>Calculation Results</h2>
            <p>Number 1: {num1}</p>
            <p>Number 2: {num2}</p>
            <p>Addition: {results['Addition']}</p>
            <p>Subtraction: {results['Subtraction']}</p>
            <p>Multiplication: {results['Multiplication']}</p>
            <p>Division: {results['Division']}</p>
            <p>Modulus: {results['Modulus']}</p>
            <p>Exponentiation: {results['Exponentiation']}</p>
            <p>Floor Division: {results['Floor Division']}</p>
            <p><strong>Results successfully stored in Firebase!</strong></p>
            <a href="/">Back</a>
        </body>
        </html>
        """
        return Response(response_html, content_type='text/html')

    except Exception as e:
        return Response(f"<p>Error: {str(e)}</p>", content_type='text/html')

def home_page(request):
    """Display a simple form to enter two numbers."""
    return Response("""
        <html>
        <head><title>Calculator</title></head>
        <body>
            <h2>Enter Two Numbers</h2>
            <form action="/calculate" method="get">
                <label>Number 1:</label>
                <input type="number" name="num1" required>
                <br><br>
                <label>Number 2:</label>
                <input type="number" name="num2" required>
                <br><br>
                <input type="submit" value="Calculate">
            </form>
        </body>
        </html>
    """, content_type='text/html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))  # Keep the port the same as before
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(home_page, route_name='home')
        config.add_route('calculate', '/calculate')
        config.add_view(calculate_and_store, route_name='calculate')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
