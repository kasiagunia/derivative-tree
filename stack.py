
class Stack:
    """Implementation of stack using python list"""
    def __init__(self):
        """Initialize items as empty list"""
        self.items = []

    def is_empty(self):
        """If stack return True, False otherwise"""
        return self.items == []

    def push(self, item):
        """Take item and append it to the top of the stack"""
        self.items.append(item)

    def pop(self):
        """Remove item from the top of the stack return it."""
        return self.items.pop()

    def peek(self):
        """Return top item of the stack"""
        return self.items[len(self.items) - 1]

    def size(self):
        """Return the size of the stack"""
        return len(self.items)

    def __str__(self):
        """Return string to print when print() method is evaluated"""
        string = ""
        for i in self.items:
            string += str(i) + ", "
        return string[:-2]