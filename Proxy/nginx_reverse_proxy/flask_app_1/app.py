from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello I am app 1 from behind the secure NGINX proxy!"

@app.route('/headers')
def headers():
    # This will display the headers NGINX injects into the request
    return jsonify(dict(request.headers))

if __name__ == '__main__':
    # Listen on all interfaces inside the container on port 5000
    app.run(host='0.0.0.0', port=5000)