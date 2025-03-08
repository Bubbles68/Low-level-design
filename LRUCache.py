class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
class LRUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.capacity = capacity
        self.left = Node(0,0)
        self.right = Node(0,0)
        self.left.next = self.right
        self.right.prev = self.left
    
    def insert(self, node):
        prev = self.right.prev
        node.prev = prev
        node.next = self.right
        prev.next = node
        self.right.prev = node

    def remove(self, node):
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            node = self.cache[key]
            self.remove(node)
            self.insert(node)
            return node.value

    def put(self, key, value):
        if key in self.cache:
            self.remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self.insert(node)
        if len(self.cache)>self.capacity:
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]

class Demo:
    def run():
        lru = LRUCache(4)
        lru.put(1,10)
        lru.put(2, 10)
        lru.get(2)
        lru.put(3, 30)
        lru.put(4, 40)
        lru.get(3)
        lru.put(5, 50)

if __name__=="__main__":
    Demo.run()