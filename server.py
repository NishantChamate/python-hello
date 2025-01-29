from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os

def calculator_view(request):
    num1 = request.params.get('num1')
    num2 = request.params.get('num2')
    
    html_template = """
    <html>
    <head>
        <title>Calculator</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; }
            .container { width: 50%; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px gray; }
            input { padding: 8px; margin: 5px; }
            .btn { padding: 10px 20px; background: #007BFF; color: white; border: none; cursor: pointer; }
            .btn:hover { background: #0056b3; }
            .results { margin-top: 20px; text-align: left; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Simple Calculator</h2>
            <form method='GET'>
                Number 1: <input type='text' name='num1' value='{num1 if num1 else ""}'><br>
                Number 2: <input type='text' name='num2' value='{num2 if num2 else ""}'><br>
                <input type='submit' value='Calculate' class='btn'>
            </form>
    """
    
    if num1 is None or num2 is None:
        return Response(html_template + "</div></body></html>")
    
    try:
        num1, num2 = int(num1), int(num2)
        addition = num1 + num2
        subtraction = num1 - num2
        multiplication = num1 * num2
        division = num1 / num2 if num2 != 0 else "undefined"
        modulus = num1 % num2 if num2 != 0 else "undefined"
        exponentiation = num1 ** num2
        floor_division = num1 // num2 if num2 != 0 else "undefined"
        
        result = f"""
            <div class='results'>
                <h3>Results:</h3>
                <p>Addition: {addition}</p>
                <p>Subtraction: {subtraction}</p>
                <p>Multiplication: {multiplication}</p>
                <p>Division: {division}</p>
                <p>Modulus: {modulus}</p>
                <p>Exponentiation: {exponentiation}</p>
                <p>Floor Division: {floor_division}</p>
            </div>
        </div>
        </body>
        </html>
        """
        
        return Response(html_template + result)
    except ValueError:
        return Response(html_template + "<p style='color:red;'>Invalid input. Please enter numeric values.</p></div></body></html>")

if __name__ == '__main__':
    port = int(os.environ.get("PORT")) 
    with Configurator() as config:
        config.add_route('calculator', '/')
        config.add_view(calculator_view, route_name='calculator')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
