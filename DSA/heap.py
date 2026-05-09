from decorators import timeit_with_message

class Heap :
    def __init__(self, heap, heap_type = 'min') :
        self.heap = heap
        self.size = len(heap)
        self.heap_type = heap_type

        if self.size > 1:
            self.heapify()

    def _parent(self, index):
        if index <= 0:
            return None
        return (index - 1) // 2

    def _left_child(self, index):
        left = 2 * index + 1
        return left if left < self.size else None

    def _right_child(self, index):
        right = 2 * index + 2
        return right if right < self.size else None

    def _compare(self, index1, index2):
        """Returns True if the element at index1 should be ABOVE index2."""
        val1 = self.heap[index1]
        val2 = self.heap[index2]
        
        if self.heap_type == 'min':
            return val1 < val2
        else:
            return val1 > val2

    def _swap(self, child_idx, parent_idx) :
        self.heap[child_idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[child_idx]

    def _heapify_up(self, index):
        while index > 0:
            parent_idx = self._parent(index)
            if self._compare(index, parent_idx):
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break

    def _heapify_down(self, index):
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            priority_node = index

            if left is not None and self._compare(left, priority_node):
                priority_node = left

            if right is not None and self._compare(right, priority_node):
                priority_node = right

            if priority_node != index:
                self._swap(priority_node, index)
                index = priority_node
            else:
                break

    @timeit_with_message(message="[HEAP-INSERT]")
    def insert(self, value) :
        self.heap.append(value)

        self.size += 1

        current_idx = self.size - 1

        self._heapify_up(current_idx)

    # def extract(self):
        

    def peek(self) :
        if self.size == 0 :
            return None
        return self.heap[0]

    @timeit_with_message(message="[HEAP-POP]")
    def pop(self) :
        if self.size == 0:
            return None
        if self.size == 1:
            self.size -= 1
            return self.heap.pop()

        min_val = self.heap[0]

        self.heap[0] = self.heap.pop()
        self.size -= 1

        self._heapify_down(0)

        return min_val

    @timeit_with_message(message="[HEAP-HEAPIFY]")
    def heapify(self):
        """Transforms self.heap into a valid Heap in O(n) time."""
        if self.size <= 1:
            return

        start_index = (self.size // 2) - 1
        
        for i in range(start_index, -1, -1):
            self._heapify_down(i)

    def __str__(self):
        if self.size == 0:
            return "Empty Heap"
        return self._build_str(0, 0)

    def _build_str(self, index, level):
        ret = ""
        right = self._right_child(index)
        left = self._left_child(index)

        if right is not None:
            ret += self._build_str(right, level + 1)

        ret += "    " * level + f"-> {self.heap[index]}\n"

        if left is not None:
            ret += self._build_str(left, level + 1)

        return ret