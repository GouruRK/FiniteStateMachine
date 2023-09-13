class Node:
    count = 0
    
    def __init__(self, initial=False, final=False):
        self.id = Node.count
        self.initial = initial
        self.final = final
        self.neighbors = set()
        Node.count += 1
    
    def connect(self, node: 'Node'):
        self.neighbors.add(node)
    
    def deconnect(self, node: 'Node'):
        if node in self.neighbors:
            self.neighbors.remove(node)
    
class Graph:
    
    def __init__(self):
        # table[id] = node
        self.node_table = {}
        # edges[id, id] = value
        self.edges = {}
    
    def cast_to_node(func):
        def cast(self, node1, node2, *args):
            if isinstance(node1, int):
                node1 = self.get_node(node1)
            if isinstance(node2, int):
                node2 = self.get_node(node2)

            return func(self, node1, node2, *args)
        return cast
        
    def get_node(self, id: int):
        if id in self.node_table:
            return self.node_table[id]
    
    def check_node(self, node: Node):
        return self.check_id(node.id)
    
    def check_id(self, id: int):
        return id in self.node_table
    
    def add_node(self, node: Node):
        if self.check_node(node):
            return
        self.node_table[node.id] = node
    
    def remove_node(self, node: int | Node):
        if not self.check_node(node):
            return
        for n in self.gen_node():
            n.deconnect(node)
            node.deconnect(n)
        self.node_table.pop(node.id)
        return n
    
    @cast_to_node
    def connect(self, start: int | Node , end: int | Node, value: str):
        if not self.check_node(start):
            self.add_node(start)
        if not self.check_node(end):
            self.add_node(end)
            
        start.connect(end)
        self.edges[(start.id, end.id)] = value

    @cast_to_node
    def deconnect(self, start: int | Node, end: int | Node):
        start.deconnect(end)
        self.edges.pop((start.id, end.id))

    def gen_id(self) -> int:
        for id in self.node_table:
            yield id
    
    def gen_node(self) -> Node:
        for node in self.node_table.values():
            yield node
    
    def gen_node_id(self) -> tuple[int, Node]:
        for infos in self.node_table.items():
            yield infos

    @cast_to_node
    def exist_path(self, start: int | Node, end: int | Node, done: set | None = None):
        if done is None:
            done = set()

        if start.id == end.id:
            return True
        if start.id in done:
            return False
        done.add(start.id)
        for node in start.neighbors:
            if self.exist_path(node, end, done):
                return True
        return False
