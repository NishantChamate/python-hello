from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("key.json")  # Load Firebase credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://caltesting-4d01d-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace with your Firebase DB URL
})

def hello_world(request):
    name = os.environ.get('NAME','Nishant')
    if not name:
        name = "world"
    
    message = "Hello, " + name + "!\n"

    # Save to Firebase
    ref = db.reference('/messages')
    ref.push({
        "name": name,
        "message": message
    })

    return Response(message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))  # Default to 8000 if PORT is not set
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
