import uuid

# =====================================================================
# THE STATEFUL COMPUTE NODE
# =====================================================================
class StatefulServerNode:
    def __init__(self, node_name: str):
        self.node_name = node_name
        
        # IN-MEMORY SESSION BOTTLENECK: State is locked to this single machine's RAM
        self._local_session_db: dict[str, dict] = {}

    def login_route(self, username: str) -> dict:
        """Simulates @app.route('/login')"""
        # 1. Generate a random unique tracking session identifier
        session_id = str(uuid.uuid4())
        
        # 2. Mutate local machine memory state
        self._local_session_db[session_id] = {
            "username": username,
            "roles": ["user"]
        }
        
        print(f"[{self.node_name}] Successfully generated session '{session_id}' in local RAM.")
        return {"session_id": session_id, "host_processed": self.node_name}

    def get_profile_route(self, session_id: str) -> dict:
        """Simulates @app.route('/get_profile')"""
        # 3. Read straight from local memory map
        if session_id in self._local_session_db:
            user_data = self._local_session_db[session_id]
            return {
                "status": "200 OK",
                "profile": f"Welcome back, {user_data['username']}!",
                "host_processed": self.node_name
            }
        
        # Lookups fail completely if the session key is missing from this single RAM heap
        return {
            "status": "401 Unauthorized",
            "error": "Session token not found on this machine context.",
            "host_processed": self.node_name
        }


# =====================================================================
# THE HORIZONTAL SCALING SIMULATION (THE FAILURE EVENT)
# =====================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("      STATEFUL HORIZONTAL SCALE TRAFFIC SIMULATION")
    print("=" * 60)

    # Deploying two identical code clones across our network
    server_node_a = StatefulServerNode("Server-Node-A")
    server_node_b = StatefulServerNode("Server-Node-B")

    print("\n--- STEP 1: User hits Load Balancer -> Routed to Node A to Login ---")
    login_response = server_node_a.login_route(username="Delwar")
    my_session_id = login_response["session_id"]
    print(f"Client Device saved Session Cookie token: {my_session_id}")

    print("\n--- STEP 2: Client makes request #2 -> Routed back to Node A ---")
    profile_response_1 = server_node_a.get_profile_route(my_session_id)
    print(f"Result: {profile_response_1['status']} | Msg: {profile_response_1.get('profile') or profile_response_1.get('error')}")

    print("\n--- STEP 3: Load Balancer switches lines -> Client routed to Node B ---")
    # Node B has the exact same routing code, but a totally separate memory heap context
    profile_response_2 = server_node_b.get_profile_route(my_session_id)
    print(f"Result: {profile_response_2['status']} | Msg: {profile_response_2.get('profile') or profile_response_2.get('error')}")
    print("=" * 60)