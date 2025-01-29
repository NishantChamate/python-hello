from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import random

def hello_world(request):
    name = os.environ.get('NAME', 'Nishant')
    if not name:
        name = "world"
    
    # Generate two random numbers
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    
    # Perform calculations
    addition = num1 + num2
    subtraction = num1 - num2
    multiplication = num1 * num2
    division = num1 / num2 if num2 != 0 else "undefined"
    modulus = num1 % num2 if num2 != 0 else "undefined"
    exponentiation = num1 ** num2
    floor_division = num1 // num2 if num2 != 0 else "undefined"
    
    message = (f"Hello, {name}!\n"
               f"Random Numbers: {num1}, {num2}\n"
               f"Addition: {addition}\n"
               f"Subtraction: {subtraction}\n"
               f"Multiplication: {multiplication}\n"
               f"Division: {division}\n"
               f"Modulus: {modulus}\n"
               f"Exponentiation: {exponentiation}\n"
               f"Floor Division: {floor_division}\n")
    
    return Response(message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))  
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
