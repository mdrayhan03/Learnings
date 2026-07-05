#############
# M -> Model
#############
class ProductModel:
    def __init__(self, name: str, category: str):
        self.name: str = name
        self.category: str = category

class ProductRepository:
    def __init__(self):
        self._products: list[ProductModel] = []
    
    def add_product(self, name: str, category: str) -> None:
        product = ProductModel(name, category)
        self._products.append(product)
        
    def fetch_all(self) -> list[ProductModel]:
        return self._products

###################
# VM -> ViewModel (The State & Binding Hub)
###################
class SearchViewModel:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo
        
        # Reactive UI State fields
        self.search_query: str = ""
        self.filtered_results: list[ProductModel] = product_repo.fetch_all()
        
        # Binding channel: Holds the callback function pointing to the View
        self.on_property_changed = None

    def set_search_query(self, query: str) -> None:
        """
        Updates the query state property and instantly filters the dataset.
        Triggers the reactive binding notification automatically.
        """
        self.search_query = query
        self._execute_search_filter()

    def _execute_search_filter(self) -> None:
        all_products = self._product_repo.fetch_all()
        
        # If query is blank, show everything, otherwise filter by case-insensitive name matches
        if not self.search_query.strip():
            self.filtered_results = all_products
        else:
            self.filtered_results = [
                p for p in all_products if self.search_query.lower() in p.name.lower()
            ]
            
        # DATA BINDING TRIGGER: Notify the view instantly that data state shifted
        if self.on_property_changed:
            self.on_property_changed()

############
# V -> View (Binds to ViewModel State)
############
class DashboardView:
    def __init__(self, search_viewmodel: SearchViewModel):
        self._viewmodel = search_viewmodel
        
        # WIRE-UP BINDING: Tell the ViewModel to automatically invoke our render method on state shifts
        self._viewmodel.on_property_changed = self.render
    
    def render(self) -> None:
        """
        The View reads state data directly from the ViewModel variables.
        It contains zero data processing or filtering logic itself.
        """
        print("\n" + "=" * 45)
        print(f"DASHBOARD VIEW (Active Query: '{self._viewmodel.search_query}')")
        print("=" * 45)
        
        if not self._viewmodel.filtered_results:
            print("  No matching products found.")
        else:
            for product in self._viewmodel.filtered_results:
                print(f"  • {product.name} [{product.category}]")
        print("=" * 45)

#############
# Simulation
#############
if __name__ == "__main__":
    print("--- 1. Initializing MVVM Architecture ---")
    # Setup data layer
    repo = ProductRepository()
    repo.add_product("iPhone 15 Pro", "Electronics")
    repo.add_product("MacBook Air M3", "Electronics")
    repo.add_product("Mechanical Keyboard", "Accessories")
    repo.add_product("Coffee Maker Express", "Home Appliances")
    
    # Setup ViewModel and pass it the data access point
    viewmodel = SearchViewModel(repo)
    
    # Setup View and bind it to the ViewModel
    view = DashboardView(viewmodel)
    
    # Initial display pass
    view.render()

    # -----------------------------------------------------------------
    # SIMULATION: Simulating a user typing into a search text field
    # -----------------------------------------------------------------
    print("\n--- 2. User types 'M' into Search input ---")
    # Notice we NEVER call view.render() explicitly! 
    # Simply changing the ViewModel state forces the screen update.
    viewmodel.set_search_query("M")
    
    print("\n--- 3. User updates input to 'MacBook' ---")
    viewmodel.set_search_query("MacBook")

    print("\n--- 4. User clears out the search input ---")
    viewmodel.set_search_query("")