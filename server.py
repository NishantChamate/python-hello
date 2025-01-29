from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os

def calculator_view(request):
    num1 = request.params.get('num1')
    num2 = request.params.get('num2')
    
    if num1 is None or num2 is None:
        return Response("<form method='GET'>
                            Number 1: <input type='text' name='num1'><br>
                            Number 2: <input type='text' name='num2'><br>
                            <input type='submit' value='Calculate'>
                        </form>")
    
    try:
        num1, num2 = int(num1), int(num2)
        addition = num1 + num2
        subtraction = num1 - num2
        multiplication = num1 * num2
        division = num1 / num2 if num2 != 0 else "undefined"
        modulus = num1 % num2 if num2 != 0 else "undefined"
        exponentiation = num1 ** num2
        floor_division = num1 // num2 if num2 != 0 else "undefined"
        
        result = (f"<p>Number 1: {num1}</p>"
                  f"<p>Number 2: {num2}</p>"
                  f"<p>Addition: {addition}</p>"
                  f"<p>Subtraction: {subtraction}</p>"
                  f"<p>Multiplication: {multiplication}</p>"
                  f"<p>Division: {division}</p>"
                  f"<p>Modulus: {modulus}</p>"
                  f"<p>Exponentiation: {exponentiation}</p>"
                  f"<p>Floor Division: {floor_division}</p>")
        
        return Response(f"<form method='GET'>
                            Number 1: <input type='text' name='num1' value='{num1}'><br>
                            Number 2: <input type='text' name='num2' value='{num2}'><br>
                            <input type='submit' value='Calculate'>
                        </form>" + result)
    except ValueError:
        return Response("Invalid input. Please enter numeric values.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))  
    with Configurator() as config:
        config.add_route('calculator', '/')
        config.add_view(calculator_view, route_name='calculator')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
