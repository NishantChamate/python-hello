from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import json
import firebase_admin
from firebase_admin import credentials, db

# Load Firebase credentials from GitHub Actions secret
firebase_key = os.getenv("FIREBASE_PRIVATE_KEY")
if firebase_key:
    firebase_key_dict = json.loads(firebase_key.replace("\\n", "\n"))
    cred = credentials.Certificate(firebase_key_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
    })

def save_to_firebase(first_value, second_value, operation, result):
    ref = db.reference("calculations")
    new_entry = ref.push()
    new_entry.set({
        "first_value": first_value,
        "second_value": second_value,
        "operation": operation,
        "result": result
    })

def hello_world(request):
    html = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculator</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f7f7f7; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .calculator { background-color: #333; border-radius: 15px; padding: 20px; box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1); }
            .calculator input { width: 100%; height: 50px; text-align: right; font-size: 24px; margin-bottom: 15px; padding: 10px; border: none; border-radius: 10px; background-color: #222; color: #fff; }
            .buttons { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
            .buttons button { padding: 20px; font-size: 24px; background-color: #444; color: white; border: none; border-radius: 10px; cursor: pointer; transition: background-color 0.3s ease, transform 0.2s ease; }
            .buttons button:hover { background-color: #666; transform: scale(1.1); }
            .buttons button:active { transform: scale(0.95); }
            .buttons button.operator { background-color: #f39c12; }
            .buttons button.clear { background-color: #e74c3c; }
            .buttons button.equals { background-color: #2ecc71; }
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
            function appendToDisplay(value) { document.getElementById('display').value += value; }
            function clearDisplay() { document.getElementById('display').value = ''; }
            function calculateResult() {
                try {
                    let expression = document.getElementById('display').value;
                    let result = eval(expression);
                    document.getElementById('display').value = result;
                    fetch('/calculate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ expression: expression, result: result })
                    });
                } catch (e) {
                    document.getElementById('display').value = 'Error';
                }
            }
        </script>
    </body>
    </html>
    """
    return Response(html)

def calculate(request):
    try:
        data = request.json_body
        expression = data.get("expression")
        result = eval(expression)
        operands = expression.split(" ")
        save_to_firebase(operands[0], operands[2], operands[1], result)
        return Response(json.dumps({"result": result}), content_type='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), content_type='application/json', status=400)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        config.add_route('calculate', '/calculate', request_method='POST')
        config.add_view(calculate, route_name='calculate', renderer='json')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
