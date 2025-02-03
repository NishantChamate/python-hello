from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
import os
import json
import firebase_admin
from firebase_admin import credentials, db
import re
import traceback

# FastAPI Application
fastapi_app = FastAPI()

class ExpressionRequest(BaseModel):
    expression: str

@fastapi_app.post("/calculate")
def calculate(request: ExpressionRequest):
    try:
        result = eval(request.expression)  # ⚠️ Avoid eval in production
        return {"result": result}
    except Exception as e:
        print(traceback.format_exc())  # Debugging
        raise HTTPException(status_code=500, detail=str(e))

# Pyramid Application
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

def save_to_firebase(expression, result):
    try:
        ref = db.reference("calculations")
        calculations = ref.get()
        next_id = len(calculations) + 1 if calculations else 1
        calc_ref = ref.child(f"calculation_{next_id}")
        calc_ref.set({"expression": expression, "result": result})
        print(f"✅ Data saved to Firebase under calculation_{next_id}")
    except Exception as e:
        print(f"❌ Error saving data to Firebase: {e}")

def hello_world(request):
    return Response("<h1>Welcome to the Calculator App</h1>")

def pyramid_calculate(request):
    try:
        data = request.json_body
        expression = data.get("expression")
        result = eval(expression)
        save_to_firebase(expression, result)
        return Response(json.dumps({"result": result}), content_type='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), content_type='application/json', status=400)

with Configurator() as config:
    config.add_route('home', '/')
    config.add_view(hello_world, route_name='home')
    config.add_route('calculate', '/calculate', request_method='POST')
    config.add_view(pyramid_calculate, route_name='calculate', renderer='json')
    pyramid_app = config.make_wsgi_app()

# Combine FastAPI and Pyramid using DispatcherMiddleware
application = DispatcherMiddleware(WSGIMiddleware(pyramid_app), {'/api': fastapi_app})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    server = make_server('0.0.0.0', port, application)
    print(f"🚀 Server running on port {port}")
    server.serve_forever()
