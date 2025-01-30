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

    # HTML with animation and CSS
    html = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f0f8ff;
                    margin: 0;
                    transition: all 0.5s ease;
                }}
                .container {{
                    text-align: center;
                    border-radius: 10px;
                    padding: 30px;
                    background-color: #fff;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 400px;
                    transform: scale(0);
                    animation: zoomIn 0.5s forwards;
                }}
                @keyframes zoomIn {{
                    0% {{ transform: scale(0); }}
                    100% {{ transform: scale(1); }}
                }}
                input[type="number"] {{
                    padding: 10px;
                    margin: 10px;
                    font-size: 14px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    width: 40%;
                }}
                button {{
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: 0.3s ease;
                }}
                button:hover {{
                    background-color: #45a049;
                }}
                .results {{
                    margin-top: 20px;
                    text-align: left;
                    display: none;
                    animation: fadeIn 0.5s forwards;
                }}
                @keyframes fadeIn {{
                    0% {{ opacity: 0; }}
                    100% {{ opacity: 1; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Simple Calculator</h2>
                <form method="GET">
                    <input type="number" name="num1" placeholder="Enter number 1" required><br>
                    <input type="number" name="num2" placeholder="Enter number 2" required><br>
                    <button type="submit">Calculate</button>
                </form>
                <div class="results" id="results">
                    <h3>Results:</h3>
                    <p>Random Numbers: {num1}, {num2}</p>
                    <p>Addition: {addition}</p>
                    <p>Subtraction: {subtraction}</p>
                    <p>Multiplication: {multiplication}</p>
                    <p>Division: {division}</p>
                    <p>Modulus: {modulus}</p>
                    <p>Exponentiation: {exponentiation}</p>
                    <p>Floor Division: {floor_division}</p>
                </div>
            </div>
            <script>
                document.querySelector("form").onsubmit = function() {{
                    document.getElementById("results").style.display = "block";
                }}
            </script>
        </body>
    </html>
    """
    return Response(html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
