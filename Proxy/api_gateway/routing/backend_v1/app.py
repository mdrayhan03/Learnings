from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/data')
def get_data():
    user = request.headers.get('X-Consumer-ID', 'Unknown')
    return jsonify({
        "version": "v1.0.0 (STABLE)",
        "server": "Standard Pool V1",
        "user": user
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)