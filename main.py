from flask import Flask, request
import hashlib
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/health', methods=['GET', 'POST'])
def healthcheck():
    if request.method == 'GET':
        return 'GET request OK!'
    data = request.get_data()
    sha256 = hashlib.sha256(data).hexdigest()
    return f'Received {len(data)} bytes with SHA256={sha256}'

