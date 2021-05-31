from flask import Flask, request
import hashlib
import yaml
import re
from api_manager import APIManager
app = Flask(__name__)
apis = APIManager()

def get_config():
    with open('/CONFIG.yml') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data

@app.route("/api", methods=['POST'])
def main():
    config = get_config()
    data = request.get_json(force=True)
    for com in config['communities']:
        if com['group_id'] != data['group_id']: continue

        # now the community matches the message

        if com['secret_key'] is not None:
            if data.get('secret') != com['secret_key']:
                print('Invalid secret key was supplied!!', data)
                return 'plz no hack 😖👉👈', 403

        if data['type'] == 'confirmation':  # this is a confirmation event, so respond with the confirmation string.
            return com['confirmation']
        if data['type'] != 'message_new':  # we cannot do anything with other types of event.
            return 'ok'

        msg = data['object']['message']
        text = msg.get('text') or ''
        private = msg['peer_id'] == msg['from_id']
        do_send = False
        if private:
            if not com['private_context_triggers']: do_send = True
            for trig in com['private_context_triggers']:
                if re.search(trig, text, flags=re.I): do_send = True
        else:
            for trig in com['public_context_triggers']:
                if re.search(trig, text, flags=re.I): do_send = True

        if do_send:
            api = apis[ com['access_key'] ]
            api = api.get_api()
            api.messages.send(peer_id=msg['peer_id'], random_id=0, message=com['text'])

        return 'ok'

    return f'Unknown community ID: {data["group_id"]}', 404

@app.route('/health', methods=['GET', 'POST'])
def healthcheck():
    if request.method == 'GET':
        return 'GET request OK!'
    data = request.get_data()
    sha256 = hashlib.sha256(data).hexdigest()
    return f'Received {len(data)} bytes with SHA256={sha256}'

