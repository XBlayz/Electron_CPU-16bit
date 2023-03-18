class Node:
    def __init__(self, info) -> None:
        self.info = info    # Data of the Node
        self.next_l = []    # List of the next Node

    def __repr__(self) -> str:
        len_ = len(self.next_l)
        if len_ == 0:
            return f"|{self.info}| -> NONE"             # If Node has no next
        if len_ == 1:
            return f"|{self.info}| -> {self.next_l[0]}" # If Node has one next
        return f"|{self.info}| -> {self.next_l}"        # If Node has more then one next

class InsGraph:
    def __init__(self) -> None:
        self.root = Node("-ROOT-")  # Root of the graph
    
    def __repr__(self) -> str:
        return self.root.__repr__() # Representation of the root
    

    def set_of_node(self) -> set[Node]:
        return InsGraph.deep_search(self.root)  # Call of the recursive deep search from the root
    
    @staticmethod
    def deep_search(root:Node) -> set[Node]:
        r = set()                                       # Initializing the result
        r.add(root)                                     # Adding the current Node to the result
        if len(root.next_l) > 0:
            for node in root.next_l:
                r.update(InsGraph.deep_search(node))    # Adding the Node of all the graph with root the next Node of the current Node
        return r
