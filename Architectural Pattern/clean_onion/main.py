from abc import ABC, abstractmethod
import json

# exceptions
class BookAlreadyBorrowedError(Exception) : pass

class BookNotFoundError(Exception) : pass

# entities (1st ring)
class Book :
    def __init__(self, book_id, title, is_borrowed):
        self.book_id = book_id
        self.title = title
        self.is_borrowed = is_borrowed
    
    def mark_as_borrowed(self) :
        if self.is_borrowed :
            raise BookAlreadyBorrowedError(f"Book: (ID: {self.book_id}){self.title} is already borrowed!")
        self.is_borrowed = True

# use cases (2nd ring)
# # outbound port
class IBookRepository(ABC) :
    @abstractmethod
    def get_by_id(self, book_id) -> Book : pass
        # raise BookNotFoundError(f"Book not found for ID: {book_id}")

    @abstractmethod
    def update(self, book: Book) -> None : pass
        # book.mark_as_borrowed()

# # usecase
class BorrowBookUseCase :
    def __init__(self, book_repo: IBookRepository):
        self.book_repo = book_repo

    def execute(self, book_id) :
        book = self.book_repo.get_by_id(book_id)
        if not book: 
            raise BookNotFoundError(f"Book not found for ID: {book_id}")
        
        book.mark_as_borrowed()
        self.book_repo.update(book)

# adapter (3rd ring)
# # outbound tools
class InMemoryBookRepository(IBookRepository) :
    def __init__(self):
        self.db = {}
    
    def get_by_id(self, book_id):
        return self.db.get(book_id)
    
    def update(self, book: Book) :
        self.db[book.book_id] = book

class LibraryController :
    def __init__(self, borrow_book_usecase: BorrowBookUseCase):
        self.borrow_book_usecase = borrow_book_usecase

    def post_borrow_request(self, request_payload: dict) :
        if request_payload.get("path") != "/borrow" :
            return json.dumps({"status": "404 Not Found", "error": "Invalid endpoint"}, indent=2)
        
        try :
            params = request_payload.get("params")
            book_id = int(params.get("book_id"))

            self.borrow_book_usecase.execute(book_id)
            return json.dumps({"status": "200 OK", "message": f"Book successfully borrowed!"}, indent=2)
        except ValueError:
            return json.dumps({"status": "400 Bad Request", "error": "Invalid Book ID format"}, indent=2)
        except BookNotFoundError as bnfe:
            return json.dumps({"status": "404 Not Found", "error": str(bnfe)}, indent=2)
        except BookAlreadyBorrowedError as babe:
            return json.dumps({"status": "409 Conflict", "error": str(babe)}, indent=2)
        except Exception as e:
            return json.dumps({"status": "500 Internal Server Error", "error": str(e)}, indent=2)
        
# outer frameworks (4th ring)
if __name__ == "__main__":
    print("--- [Initialization] Setting up Clean Architecture Rings ---")
    
    # 1. Instantiate Infrastructure (Ring 4 -> Ring 3)
    repo = InMemoryBookRepository()
    
    # Prepopulate database with 2 books as requested by specifications
    repo.update(Book(book_id=101, title="Clean Architecture", is_borrowed=False))
    repo.update(Book(book_id=102, title="The Hobbit", is_borrowed=True))
    
    # 2. Instantiate Use Case & Inject Repository (Ring 3 -> Ring 2)
    use_case = BorrowBookUseCase(repo)
    
    # 3. Instantiate Controller & Inject Use Case (Ring 2 -> Ring 3)
    controller = LibraryController(use_case)
    
    print("System setup complete. Running simulation tests...\n")

    # -----------------------------------------------------------------
    # TEST 1: Borrow an available book
    # -----------------------------------------------------------------
    req1 = {"path": "/borrow", "params": {"book_id": "101"}}
    print("--- TEST 1: Borrowing Available Book (ID: 101) ---")
    print(controller.post_borrow_request(req1))
    print("-" * 50)

    # -----------------------------------------------------------------
    # TEST 2: Borrow a book that is already borrowed
    # -----------------------------------------------------------------
    req2 = {"path": "/borrow", "params": {"book_id": "102"}}
    print("\n--- TEST 2: Borrowing Already Borrowed Book (ID: 102) ---")
    print(controller.post_borrow_request(req2))
    print("-" * 50)

    # -----------------------------------------------------------------
    # TEST 3: Borrow a non-existent book
    # -----------------------------------------------------------------
    req3 = {"path": "/borrow", "params": {"book_id": "999"}}
    print("\n--- TEST 3: Borrowing Missing Book (ID: 999) ---")
    print(controller.post_borrow_request(req3))
    print("-" * 50)