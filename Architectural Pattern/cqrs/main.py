import json

class TitleError(Exception): pass
class ContentError(Exception): pass
class ArticleNotFoundError(Exception): pass

class Article :
    def __init__(self, article_id: int, title: str, content: str) -> None:
        self.article_id = article_id
        self.title = title
        self.content = content

# shared state
class ArticleRepository:
    def __init__(self):
        self._db = {}
    
    def save(self, article: Article) -> None:
        self._db[article.article_id] = article

    def get_by_id(self, article_id: int) -> Article:
        article = self._db.get(article_id)
        if not article :
            raise ArticleNotFoundError(f"Article(ID: {article_id}) not found!")
        return article

class ArticleValidator :
    def validate(self, title, content) -> bool :
        if not title or len(title) == 0 :
            raise TitleError("Title can't be None or Empty!")
        
        if not content or len(content) <= 10 :
            raise ContentError("Content can be less then 10 character!")
        
        return True

# command
class ArticleCommandHandler :
    def __init__(self, aritlcle_repo: ArticleRepository, article_validator: ArticleValidator):
        self.aritlcle_repo = aritlcle_repo
        self.article_validator = article_validator
    def handle_create_article(self, article_id: int, title: str, content: str) :
        if self.article_validator.validate(title, content) :
            article = Article(article_id, title, content)
            self.aritlcle_repo.save(article)
            return True
        
# query
class ArticleQueryHandler :
    def __init__(self, article_repo: ArticleRepository):
        self.article_repo = article_repo
    def get_article_view(self, article_id: int) -> dict :
        try :
            article = self.article_repo.get_by_id(article_id)
            return json.dumps({
                "status": "200 OK",
                "payload": {
                    "article_id": article.article_id,
                    "title": article.title,
                    "content": article.content
                }
            }, indent=2)
        except ArticleNotFoundError as anfe :
            return json.dumps({
        "status": "404 Not Found",
        "payload": {
            "error": str(anfe),
        }
    }, indent=2)
    
# execution
if __name__ == "__main__" :
    print("--- [Initialization] Setting up CQRS Handlers ---")
    
    # 1. Instantiate the single source of truth (Shared Repository)
    shared_repo = ArticleRepository()
    validator = ArticleValidator()
    
    # 2. Instantiate Command and Query sides completely separated, injecting the repo
    command_handler = ArticleCommandHandler(shared_repo, validator)
    query_handler = ArticleQueryHandler(shared_repo)

    print("System ready.\n")
    # -----------------------------------------------------------------
    # SIMULATION 1: Successfully Creating Articles (Commands)
    # -----------------------------------------------------------------
    print("--- 1. Executing Write Commands ---")
    try:
        command_handler.handle_create_article(
            article_id=1, 
            title="Learning CQRS", 
            content="CQRS splits your reads and writes beautifully."
        )
        command_handler.handle_create_article(
            article_id=2, 
            title="Python Architecture", 
            content="Clean code starts with great architecture choices."
        )
        print("[Success] Commands processed and data saved.")
    except Exception as e:
        print(f"[Command Error] {e}")

    print("-" * 60)

    # -----------------------------------------------------------------
    # SIMULATION 2: Reading Articles Back (Queries)
    # -----------------------------------------------------------------
    print("\n--- 2. Executing Read Queries ---")
    try:
        view_1 = query_handler.get_article_view(1)
        view_2 = query_handler.get_article_view(2)
        
        print(f"Article 1 View: {view_1}")
        print(f"Article 2 View: {view_2}")
    except Exception as e:
        print(f"[Query Error] {e}")

    print("-" * 60)

    # -----------------------------------------------------------------
    # SIMULATION 3: Command Validation Failure
    # -----------------------------------------------------------------
    print("\n--- 3. Testing Command Validation Failure ---")
    try:
        command_handler.handle_create_article(
            article_id=3, 
            title="Short", 
            content="Too short" # Will trigger ContentError (< 10 chars)
        )
    except (TitleError, ContentError) as validation_err:
        print(f"[Expected Validation Exception Caught]: {validation_err}")