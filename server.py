import firebase_admin
from firebase_admin import credentials, firestore
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

# Initialize Firebase
cred = credentials.Certificate("path/to/your-firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def calculate_and_store(request):
    try:
        num1 = int(request.GET.get('num1', 0))
        num2 = int(request.GET.get('num2', 0))

        results = {
            "Addition": num1 + num2,
            "Subtraction": num1 - num2,
            "Multiplication": num1 * num2,
            "Division": num1 / num2 if num2 != 0 else "undefined",
        }

        # Store results in Firebase
        db.collection("calculations").add(results)

        return Response(f"Results stored successfully: {results}")

    except Exception as e:
        return Response(f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('calculate', '/calculate')
        config.add_view(calculate_and_store, route_name='calculate')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
