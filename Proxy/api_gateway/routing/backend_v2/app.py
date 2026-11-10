from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/data')
def get_data():
    user = request.headers.get('X-Consumer-ID', 'Unknown')
    return jsonify({
        "version": "v2.0.0 (CANARY CANDIDATE)",
        "server": "Canary Pool V2",
        "user": user,
        "new_feature_preview": "Active"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)