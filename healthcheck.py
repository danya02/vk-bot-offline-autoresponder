import requests
import os
import hashlib
import random

req = requests.get('http://localhost:8000/health')
if req.text != 'GET request ok!':
    print('GET check failed: got', repr(req.text))
    raise SystemExit(1)

data = os.urandom(random.randint(16, 4096))
sha256 = hashlib.sha256(data).hexdigest()
req = requests.post('http://localhost:8000/health', data=data)
expected = f'Received {len(data)} bytes with SHA256={sha256}'
if req.text != expected:
    print('POST check failed: sent', data, 'expected', repr(expected), 'got', repr(req.text))
    raise SystemExit(1)

