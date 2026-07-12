from flask import Flask, request, jsonify, make_response
import time

app = Flask(__name__)

@app.route('/')
def home():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    response = make_response(f"Hello from Backend! Current server time is: {current_time}\n")
    # Tell NGINX it can cache this response for 15 seconds
    response.headers['Cache-Control'] = 'public, max-age=15'
    return response

@app.route('/headers')
def headers():
    # This will display the headers NGINX injects into the request
    return jsonify(dict(request.headers))

if __name__ == '__main__':
    # Listen on all interfaces inside the container on port 5000
    app.run(host='0.0.0.0', port=5000)