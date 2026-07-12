import base64
import json
import time
import hmac
import hashlib

# =====================================================================
# THE STATELESS COMPUTE NODE
# =====================================================================
class StatelessServerNode:
    def __init__(self, node_name: str, secret_key: str):
        self.node_name = node_name
        self.secret_key = secret_key  # Shared system key across clusters

    def _generate_signature(self, serialized_payload: str) -> str:
        """Creates a secure hash of the payload using our secret key."""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            serialized_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def login_route(self, username: str) -> dict:
        """Simulates @app.route('/login')"""
        # 1. Prepare raw state data payload
        payload = {
            "username": username,
            "exp": time.time() + 3600
        }
        
        # 2. Serialize and prepare cryptographically verifiable token package
        serialized = json.dumps(payload)
        signature = self._generate_signature(serialized)
        
        # Combine the clean data and signature token footprint together
        token_package = {"data": serialized, "signature": signature}
        token_bytes = json.dumps(token_package).encode('utf-8')
        
        # Base64 encode the final package safely for transport string transfer
        session_token = base64.b64encode(token_bytes).decode('utf-8')
        
        print(f"[{self.node_name}] Generated secure stateless token for '{username}'. RAM remains empty.")
        return {"session_token": session_token, "host_processed": self.node_name}

    def get_profile_route(self, session_token: str) -> dict:
        """Simulates @app.route('/get_profile')"""
        try:
            # 1. Reverse the Base64 transport encoding layer
            token_bytes = base64.b64decode(session_token.encode('utf-8'))
            token_package = json.loads(token_bytes.decode('utf-8'))
            
            serialized_data = token_package["data"]
            client_signature = token_package["signature"]
            
            # 2. THE CRITICAL BOUNDARY GUARD: Verify the signature has not been modified
            expected_signature = self._generate_signature(serialized_data)
            if not hmac.compare_digest(client_signature, expected_signature):
                return {"status": "401 Unauthorized", "error": "Token signature tampered with!", "host_processed": self.node_name}
            
            # 3. Decode the state variables straight out of the validated string
            user_data = json.loads(serialized_data)
            
            # Check expiration timeline state
            if time.time() > user_data["exp"]:
                return {"status": "401 Unauthorized", "error": "Token has expired.", "host_processed": self.node_name}
                
            return {
                "status": "200 OK",
                "profile": f"Welcome back, {user_data['username']}!",
                "host_processed": self.node_name
            }
        except Exception:
            return {"status": "400 Bad Request", "error": "Malformed token container structure.", "host_processed": self.node_name}


# =====================================================================
# THE STATELESS HORIZONTAL TRAFFIC SIMULATION
# =====================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("      STATELESS HORIZONTAL SCALE TRAFFIC SIMULATION")
    print("=" * 60)

    # Both nodes share the same global signature verification key secret
    CLUSTER_SECRET = "super_secure_janatawifi_production_secret_key"

    # Deploying two totally isolated server instances
    server_node_a = StatelessServerNode("Server-Node-A", CLUSTER_SECRET)
    server_node_b = StatelessServerNode("Server-Node-B", CLUSTER_SECRET)

    print("\n--- STEP 1: User hits Load Balancer -> Routed to Node A to Login ---")
    login_response = server_node_a.login_route(username="Delwar")
    my_token = login_response["session_token"]
    print(f"Client Device saved Token: {my_token[:30]}...[truncated]")

    print("\n--- STEP 2: Client makes request #2 -> Routed back to Node A ---")
    profile_response_1 = server_node_a.get_profile_route(my_token)
    print(f"Result: {profile_response_1['status']} | Msg: {profile_response_1.get('profile') or profile_response_1.get('error')} | Node: {profile_response_1['host_processed']}")

    print("\n--- STEP 3: Load Balancer switches lines -> Client routed to Node B ---")
    # Node B reads the signature securely, completely independently without contacting Node A!
    profile_response_2 = server_node_b.get_profile_route(my_token)
    print(f"Result: {profile_response_2['status']} | Msg: {profile_response_2.get('profile') or profile_response_2.get('error')} | Node: {profile_response_2['host_processed']}")
    
    print("\n--- STEP 4: Simulating Malicious Tampering Exploit Attempt ---")
    # A hacker intercepts the token, changes payload value and creates a fake profile query
    tampered_token = base64.b64encode(json.dumps({"data": '{"username": "Admin", "exp": 9999999999}', "signature": "fake_signature_hash"}).encode('utf-8')).decode('utf-8')
    hack_response = server_node_b.get_profile_route(tampered_token)
    print(f"Result: {hack_response['status']} | Error: {hack_response.get('error')} | Node: {hack_response['host_processed']}")
    print("=" * 60)