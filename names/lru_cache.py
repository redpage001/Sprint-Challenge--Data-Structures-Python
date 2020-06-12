class ListNode:
    def __init__(self, key, value, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next

    def insert_after(self, value):
        current_next = self.next
        self.next = ListNode(value, self, current_next)
        if current_next:
            current_next.prev = self.next

    def insert_before(self, value):
        current_prev = self.prev
        self.prev = ListNode(value, current_prev, self)
        if current_prev:
            current_prev.next = self.prev

    def delete(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev

class DoublyLinkedList:
    def __init__(self, node=None):
        self.head = node
        self.tail = node
        self.length = 1 if node is not None else 0

    def __len__(self):
        return self.length

    def add_to_head(self, new_node):
        self.length += 1
        if not self.head and not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def remove_from_head(self):
        if not self.head:
            return None
        elif self.head is self.tail:
            self.length -= 1
            head_value = self.head.value
            self.head = None
            self.tail = None
            return head_value
        else:
            self.length -= 1
            new_head = self.head.next
            old_head = self.head.value
            self.head = new_head
            self.head.prev.delete()
            return old_head

    def add_to_tail(self, new_node):
        self.length += 1
        if not self.head and not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def remove_from_tail(self):
        if not self.tail:
            return None
        elif self.tail is self.head:
            self.length -= 1
            tail_value = self.tail.value
            self.head = None
            self.tail = None
            return tail_value
        else:
            self.length -= 1
            new_tail = self.tail.prev
            old_tail = self.tail.value
            self.tail = new_tail
            self.tail.next.delete()
            return old_tail

    def move_to_front(self, node):
        if node is self.head:
            return None
        else:
            if node is self.tail:
                self.tail = self.tail.prev
            node_value = node.value
            node.delete()
            self.head.insert_before(node_value)
            self.head = self.head.prev

    def move_to_end(self, node):
        if node is self.tail:
            return None
        else:
            if node is self.head:
                self.head = self.head.next
            node_value = node.value
            node.delete()
            self.tail.insert_after(node_value)
            self.tail = self.tail.next

    def delete(self, node):
        if not self.head and not self.tail:
            return None
        elif self.head is self.tail:
            self.head = None
            self.tail = None
            self.length -= 1
        elif node is self.head:
            self.head = self.head.next
            self.length -= 1
            node.delete()
        elif node is self.tail:
            self.tail = self.tail.prev
            self.length -= 1
            node.delete()
        else:
            self.length -= 1
            node.delete()
        
    def get_max(self):
        if self.head is None:
            return None
        
        max_so_far = self.head.value

        current = self.head.next

        while current is not None:
            if current.value > max_so_far:
                max_so_far = current.value

            current = current.next

        return max_so_far

class LRUCache:
    """
    Our LRUCache class keeps track of the max number of nodes it
    can hold, the current number of nodes it is holding, a doubly-
    linked list that holds the key-value entries in the correct
    order, as well as a storage dict that provides fast access
    to every node stored in the cache.
    """
    def __init__(self, limit=10):
        if limit <= 0:
            print("Limit must be greater than 0")
        self.storage = {}
        self.list = DoublyLinkedList()
        self.limit = limit
        self.current_size = 0

    """
    Retrieves the value associated with the given key. Also
    needs to move the key-value pair to the end of the order
    such that the pair is considered most-recently used.
    Returns the value associated with the key or None if the
    key-value pair doesn't exist in the cache.
    """
    def get(self, key):
        if key not in self.storage:
            return None
        node = self.storage[key]

        if self.list.head == node:
            return node.value
        self.list.delete(node)
        self.list.add_to_head(node)
        return key

    """
    Adds the given key-value pair to the cache. The newly-
    added pair should be considered the most-recently used
    entry in the cache. If the cache is already at max capacity
    before this entry is added, then the oldest entry in the
    cache needs to be removed to make room. Additionally, in the
    case that the key already exists in the cache, we simply
    want to overwrite the old value associated with the key with
    the newly-specified value.
    """
    def set(self, key, value):
        if key in self.storage:
            node = self.storage[key]
            node.value = value

            if self.list.head != node:
                deleted_node = node
                self.list.delete(node)
                self.list.add_to_head(deleted_node)
        else:
            new_node = ListNode(key, value)
            if self.current_size == self.limit:
                del self.storage[self.list.tail.key]
                self.list.delete(self.list.tail)
            self.list.add_to_head(new_node)
            self.storage[key] = new_node
            self.current_size += 1
