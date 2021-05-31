from flask import Flask, request
import hashlib
import yaml
from api_manager import APIManager
app = Flask(__name__)
apis = APIManager()

def get_config():
    with open('/CONFIG.yml') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data

@app.route("/", methods=['POST'])
def hello():
    config = get_config()
    print(config)
    return 'HelloWorld'

@app.route('/health', methods=['GET', 'POST'])
def healthcheck():
    if request.method == 'GET':
        return 'GET request OK!'
    data = request.get_data()
    sha256 = hashlib.sha256(data).hexdigest()
    return f'Received {len(data)} bytes with SHA256={sha256}'

