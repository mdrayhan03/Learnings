# backend/app.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/v1/data')
def get_data():
    # The gateway injects who this user is after validating their API key
    consumer_id = request.headers.get('X-Consumer-ID', 'Unknown')
    return {
        "status": "success",
        "message": "Welcome to the secure internal data cluster!",
        "authenticated_as": consumer_id
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)