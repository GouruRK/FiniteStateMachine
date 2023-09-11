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
        self.edges = {}
    
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
    
    def remove_node(self, node: Node):
        if not self.check_node(node):
            return
        for n in self.node_table.items():
            n.deconnect(node)
            node.deconnect(n)
        return n
    
    def connect(self, start: Node, end: Node, value: str):
        if not self.check_node(start):
            self.add_node(start)
        if not self.check_node(end):
            self.add_node(end)
        start.connect(end)
        self.edges[(start.id, end.id)] = value
        
    def connect_id(self, start: int, end: int, value: str):
        if not (start in self.node_table) and (end in (self.node_table)):
            return
        self.get_node(start).connect(self.get_node(end))
        self.edges[(start, end)] = value

    def deconnect(self, start: Node, end: Node):
        if (not self.check_node(start)) or (not self.check_node(end)):
            return
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
