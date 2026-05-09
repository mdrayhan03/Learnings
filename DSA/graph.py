from collections import deque

class Graph:
    def __init__(self, is_weighted, is_directed) :
        self.is_weighted = is_weighted
        self.is_directed = is_directed

        self.adj = {}

    def add_vertex(self, vertex_id) :
        self.adj[vertex_id] = {}

    def add_edge(self, u, v, weight=1) :
        if u not in self.adj :
            self.add_vertex(u)
        if v not in self.adj :
            self.add_vertex(v)

        self.adj[u][v] = weight

        if not self.is_directed :
            self.adj[v][u] = weight
    
    def get_neighbors(self, vertex_id) :
        if vertex_id not in self.adj:
            return []
            
        return list(self.adj[vertex_id].keys())
    
    def get_weight(self, u, v) :
        if u not in self.adj or v not in self.adj :
            return None
        
        return self.adj[u][v]
    
    def bfs(self, start_node) :
        if start_node not in self.adj :
            return []
        
        visited = {start_node}
        queue = deque([start_node])
        order = []

        while queue:
            current = queue.popleft()
            order.append(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return order
    
    def dfs(self, start_node, visited=None) :
        if visited is None:
            visited = set()
        
        if start_node not in self.adj:
            return []

        visited.add(start_node)
        traversal_order = [start_node]

        for neighbor in self.get_neighbors(start_node):
            if neighbor not in visited:
                traversal_order.extend(self.dfs(neighbor, visited))
        
        return traversal_order
        
    def get_in_degree(self, vertex_id) :
        if vertex_id not in self.adj:
            return 0
        
        if not self.is_directed:
            return len(self.adj[vertex_id])
        
        count = 0
        for u in self.adj:
            if vertex_id in self.adj[u]:
                count += 1
        return count
    
    def has_cycle(self):
        visited = set()

        rec_stack = set() if self.is_directed else None

        for node in self.adj:
            if node not in visited:
                if self._has_cycle_util(node, visited, rec_stack, None):
                    return True
        return False

    def _has_cycle_util(self, v, visited, rec_stack, parent):
        visited.add(v)
        
        if self.is_directed:
            rec_stack.add(v)

        for neighbor in self.get_neighbors(v):
            if self.is_directed:
                if neighbor in rec_stack:
                    return True
                if neighbor not in visited:
                    if self._has_cycle_util(neighbor, visited, rec_stack, v):
                        return True
            else:
                if neighbor not in visited:
                    if self._has_cycle_util(neighbor, visited, None, v):
                        return True
                elif neighbor != parent:
                    return True

        if self.is_directed:
            rec_stack.remove(v)
        return False
    
    def topological_sort(self):
        # kahn's approach (bfs)
        if not self.is_directed:
            print("Topological Sort is only defined for directed graphs.")
            return None
        
        in_degree = {u: self.get_in_degree(u) for u in self.adj}

        queue = deque([u for u in in_degree if in_degree[u] == 0])
        
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)

            for v in self.get_neighbors(u):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo_order) != len(self.adj):
            print("Graph has a cycle! Topological sort not possible.")
            return None

        return topo_order
    
# Test
# print("--- Test 1: Undirected Social Network ---")
# social = Graph(is_weighted=False, is_directed=False)
# social.add_edge("Alice", "Bob")
# social.add_edge("Alice", "Charlie")
# social.add_edge("Bob", "David")

# print(f"Alice's neighbors: {social.get_neighbors('Alice')}") # Should be ['Bob', 'Charlie']
# print(f"BFS from Alice: {social.bfs('Alice')}")            # Order of discovery
# print(f"Is there a cycle? {social.has_cycle()}")            # Should be False

# print("\n--- Test 2: Directed Task Scheduling ---")
# tasks = Graph(is_weighted=False, is_directed=True)
# # Logic: Wake up -> Drink Coffee -> Work. Also Wake up -> Get Dressed.
# tasks.add_edge("Wake Up", "Drink Coffee")
# tasks.add_edge("Wake Up", "Get Dressed")
# tasks.add_edge("Drink Coffee", "Work")
# tasks.add_edge("Get Dressed", "Work")

# print(f"In-degree of 'Work': {tasks.get_in_degree('Work')}") # Should be 2
# print(f"Topological Sort: {tasks.topological_sort()}")       # Valid linear order

# # Test Cycle Detection
# tasks.add_edge("Work", "Wake Up") # Creates a loop
# print(f"Cycle detected after loop added? {tasks.has_cycle()}") # Should be True
# print(f"Topo sort with cycle: {tasks.topological_sort()}")     # Should print error & return None

print("\n--- Test 3: Weighted Map ---")
gps = Graph(is_weighted=True, is_directed=False)
gps.add_edge("Home", "Office", 15)
gps.add_edge("Office", "Gym", 10)

print(f"Distance Home -> Office: {gps.get_weight('Home', 'Office')}") # Should be 15
print(f"Distance Office -> Home: {gps.get_weight('Office', 'Home')}") # Should be 15 (due to Undirected)