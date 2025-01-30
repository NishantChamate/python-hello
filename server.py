from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK with correct key path
cred = credentials.Certificate("key.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://caltesting-4d01d-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace with actual Firebase URL
})

def hello_world(request):
    try:
        name = os.environ.get('NAME', "world")
        message = "Hello, " + name + "!\n"

        # Save to Firebase
        ref = db.reference('/messages')
        ref.push({"name": name, "message": message})

        return Response(message)
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Defaults to 8000 if PORT is not set
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello', renderer="string")
        app = config.make_wsgi_app()
    
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
