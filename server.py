from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os

def hello_world(request):
    name = os.environ.get('NAME', 'Nishant')
    if name is None or len(name) == 0:
        name = "world"
    message = "Hello, " + name + "!\n"
    return Response(message)

def calculate(request):
    try:
        num1 = float(request.params.get('num1', 0))
        num2 = float(request.params.get('num2', 1))  # Default to 1 to avoid zero division error
        operation = request.params.get('operation', 'add')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return Response("Error: Division by zero is not allowed.")
            result = num1 / num2
        else:
            return Response("Error: Unsupported operation.")

        return Response(f"Result: {result}\n")
    except ValueError:
        return Response("Error: Invalid input.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))  
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')

        config.add_route('calculate', '/calculate')
        config.add_view(calculate, route_name='calculate')
        
        app = config.make_wsgi_app()
    
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
