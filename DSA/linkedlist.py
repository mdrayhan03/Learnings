class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class SingleLinkedList:
    def __init__(self):
        self.head = None
    
    def put(self, key, value):
        """
        Handles both Insertion and Updating (Upsert).
        Returns True if a NEW node was added, False if an existing key was updated.
        """
        temp = self.head
        while temp:
            if temp.key == key:
                temp.value = value
                return False 
            temp = temp.next
        
        new_node = Node(key, value)
        new_node.next = self.head
        self.head = new_node
        return True

    def read(self, key):
        temp = self.head
        while temp:
            if temp.key == key:
                return temp.value
            temp = temp.next
        return None

    def delete(self, key):
        temp = self.head
        prev = None

        while temp:
            if temp.key == key:
                if prev is None:
                    self.head = temp.next
                else:
                    prev.next = temp.next
                return True
            prev = temp
            temp = temp.next
        return False

    def contains(self, key):
        temp = self.head
        while temp:
            if temp.key == key:
                return True
            temp = temp.next
        return False