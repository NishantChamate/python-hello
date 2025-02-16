from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os

def hello_world(request):
    html = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .calculator {
                background-color: #333;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            }
            .calculator input {
                width: 100%;
                height: 50px;
                text-align: right;
                font-size: 24px;
                margin-bottom: 15px;
                padding: 10px;
                border: none;
                border-radius: 10px;
                background-color: #222;
                color: #fff;
            }
            .buttons {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
            }
            .buttons button {
                padding: 20px;
                font-size: 24px;
                background-color: #444;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            .buttons button:hover {
                background-color: #666;
                transform: scale(1.1);
            }
            .buttons button:active {
                transform: scale(0.95);
            }
            .buttons button.operator {
                background-color: #f39c12;
            }
            .buttons button.clear {
                background-color: #e74c3c;
            }
            .buttons button.equals {
                background-color: #2ecc71;
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <input id="display" type="text" disabled />
            <div class="buttons">
                <button onclick="appendToDisplay('7')">7</button>
                <button onclick="appendToDisplay('8')">8</button>
                <button onclick="appendToDisplay('9')">9</button>
                <button onclick="appendToDisplay('+')" class="operator">+</button>
                
                <button onclick="appendToDisplay('4')">4</button>
                <button onclick="appendToDisplay('5')">5</button>
                <button onclick="appendToDisplay('6')">6</button>
                <button onclick="appendToDisplay('-')" class="operator">-</button>
                
                <button onclick="appendToDisplay('1')">1</button>
                <button onclick="appendToDisplay('2')">2</button>
                <button onclick="appendToDisplay('3')">3</button>
                <button onclick="appendToDisplay('*')" class="operator">*</button>
                
                <button onclick="appendToDisplay('0')">0</button>
                <button onclick="clearDisplay()" class="clear">C</button>
                <button onclick="calculateResult()" class="equals">=</button>
                <button onclick="appendToDisplay('/')" class="operator">/</button>
            </div>
        </div>
        <script>
            function appendToDisplay(value) {
                document.getElementById('display').value += value;
            }

            function clearDisplay() {
                document.getElementById('display').value = '';
            }

            function calculateResult() {
                try {
                    let result = eval(document.getElementById('display').value);
                    document.getElementById('display').value = result;
                } catch (e) {
                    document.getElementById('display').value = 'Error';
                }
            }
        </script>
    </body>
    </html>
    """
    return Response(html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
