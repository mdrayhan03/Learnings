from DSA.linkedlist import SingleLinkedList
from decorators import timeit_with_message

class HashMap:
    def __init__(self, capacity=10, load_factor_threshold=0.75):
        self.capacity = capacity
        self.buckets = [SingleLinkedList() for _ in range(capacity)]
        self.size = 0
        self.load_factor_threshold = load_factor_threshold
        self.rehashed = 0

    def hash_function(self, key):
        if isinstance(key, int):
            return key % self.capacity
        
        hash_value = 0
        for char in str(key):
            hash_value = (hash_value * 31 + ord(char)) % self.capacity
        return hash_value
    
    def builtin_hash_function(self, key):
        return abs(hash(key)) % self.capacity
    
    def insert(self, key, value):
        """
        Public insert method that triggers rehashing if the map is too full.
        """
        self.need_rehash()
        
        index = self.hash_function(key)
        is_new_node = self.buckets[index].put(key, value)
        
        if is_new_node:
            self.size += 1
        
        return True
    
    def read(self, key):
        index = self.hash_function(key)
        return self.buckets[index].read(key)
    
    def update(self, key, value):
        index = self.hash_function(key)
        return not self.buckets[index].put(key, value)
    
    def delete(self, key):
        index = self.hash_function(key)
        response = self.buckets[index].delete(key)
        if response:
            self.size -= 1
        return response
    
    def load_factor(self):
        return self.size / self.capacity
    
    def need_rehash(self):
        if self.load_factor() >= self.load_factor_threshold:
            print(f"[HM-REHASH] -> Load factor {self.load_factor():.2f} reached. Starting...")
            self.rehash()
            return True
        return False

    @timeit_with_message(message="[HM-REHASH]")
    def rehash(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [SingleLinkedList() for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            temp = bucket.head
            while temp:
                index = self.hash_function(temp.key)
                
                if self.buckets[index].put(temp.key, temp.value):
                    self.size += 1
                temp = temp.next

        self.rehashed += 1
    
    def contains(self, key):
        return self.read(key) is not None
    
import time

# Create two HashMaps with 10,000 items
# We'll trigger a rehash by setting capacity to 5,000
test_size = 50000 
hm_recursive = HashMap(capacity=5000)
hm_direct = HashMap(capacity=5000)

# 1. Benchmark: Using self.insert()
start = time.time()
for i in range(test_size):
    hm_recursive.insert(f"key_{i}", i)
end = time.time()
print(f"Total time with self.insert(): {end - start:.4f}s")

# 2. Benchmark: Using Direct Bucket Move
# (Assume we modified the rehash method to use bucket.put directly)
start = time.time()
for i in range(test_size):
    hm_direct.insert(f"key_{i}", i)
end = time.time()
print(f"Total time with Direct SLL Move: {end - start:.4f}s")