from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/data')
def get_data():
    # Downstream service reads headers injected by Gateway
    consumer_id = request.headers.get('X-Consumer-ID', 'Unknown')
    correlation_id = request.headers.get('X-Correlation-ID', 'None')
    
    # Return payload containing both public and internal/sensitive metadata
    return jsonify({
        "message": "Welcome to the secure internal data cluster!",
        "authenticated_as": consumer_id,
        "correlation_id": correlation_id,
        # Sensitive fields that the Gateway should sanitize/remove:
        "internal_db_host": "db-cluster-node-04.internal",
        "debug_trace": "SQL execution took 12ms on shard_3"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)