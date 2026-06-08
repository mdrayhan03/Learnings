import json

class User:
    def __init__(self, user_id, name, rating):
        self.user_id = user_id
        self.name = name
        self.rating = rating

class UserRepository:
    def __init__(self):
        self._db = {}
    
    def save(self, user:User) :
        self._db[user.user_id] = user
    
    def get_by_id(self, user_id: int) -> User:
        return self._db.get(user_id)

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def receive_internal_network_call(self, endpoint_url: str) :
        user_id = int(endpoint_url.split("/")[-1])

        user = self.user_repo.get_by_id(user_id)

        return json.dumps({
            "status" : "200 OK",
            "payload" : {
                "user_id" : user.user_id,
                "name" : user.name,
                "rating" : user.rating,
            },
        }, indent=2)