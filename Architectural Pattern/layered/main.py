import json

# Define a clean custom domain exception
class ProductNotFoundError(Exception):
    pass

# data layer
class ProductRepository :
    def __init__(self):
        self.db = [
            {"id": 1, "name": "Product 1", "base_price": 10},
            {"id": 2, "name": "Product 2", "base_price": 10},
            {"id": 3, "name": "Product 3", "base_price": 10},
        ]
    
    def get(self, product_id):
        for product in self.db :
            if product.get("id") == product_id :
                return product
        return None
    
# business layer
class ProductService :
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product_price(self, product_id: int, is_premium: bool) -> dict :
        product = self.repository.get(product_id)

        if product is None :
            raise ProductNotFoundError(f"Product for id: {product_id} not found")
        
        base_price = product["base_price"]
        discounted_price = base_price
        if is_premium :
            discounted_price = base_price - (base_price * 0.1)

        return {
            "id": product["id"],
            "name": product["name"],
            "base_price": base_price,
            "discounted_price": discounted_price,
        }
    
# presentation layer
class ProductController :
    def __init__(self, service: ProductService):
        self.service = service

    def handle_request(self, http_request: dict) :
        if http_request.get("path") != "/product":
            return json.dumps({"status": "404 Not Found", "error": "Invalid Endpoint"})

        try :
            params = http_request.get("params", {})

            product_id = int(params.get("id"))
            is_premium = params.get("premium") == "true"

            product_data = self.service.get_product_price(product_id, is_premium)
            return json.dumps({"status" : "200 OK", "data" : product_data}, indent=2)
        except ValueError:
            # Catches issues if 'id' cannot be parsed to an integer
            return json.dumps({"status": "400 Bad Request", "error": "Invalid ID format"})
        except ProductNotFoundError as pne:
            # Specifically catches missing products from business logic
            return json.dumps({"status": "404 Not Found", "error": str(pne)})
        except Exception as e:
            return json.dumps({"status": "500 Internal Server Error", "error": str(e)})

# ==========================================
# SIMULATION TESTING
# ==========================================
if __name__ == "__main__":
    repo = ProductRepository()
    service = ProductService(repo)
    controller = ProductController(service)

    # Test 1: Successful Premium Request
    req1 = {"path": "/product", "params": {"id": "2", "premium": "true"}}
    print("--- TEST 1: Premium User ---")
    print(controller.handle_request(req1))

    # Test 2: Missing Product Request
    req2 = {"path": "/product", "params": {"id": "99", "premium": "false"}}
    print("\n--- TEST 2: Missing Product ---")
    print(controller.handle_request(req2))