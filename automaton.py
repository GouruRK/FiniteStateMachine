from graph import Graph, Node

class FSM:
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.initials = set()
        self.finals = set()
        for node in graph.gen_node():
            self.add_sub_set(node)
    
    def add_sub_set(self, node: Node):
        if node.initial:
            self.initials.add(node)
        if node.final:
            self.finals.add(node)

    def remove_node_sub_set(self, node: Node):
        if node in self.initials:
            self.initials.pop(node)
        if node in self.finals:
            self.finals.pop(node)
    
    def add_node(self, node: Node):
        self.add_sub_set(node)
        self.graph.add_node(node)
    
    def remove_node(self, node: Node):
        self.remove_node_sub_set(node)
        self.graph.remove_node(node)
    
    def connect(self, start: Node, end: Node, value: str):
        self.add_sub_set(start)
        self.add_sub_set(end)
        self.graph.connect(start, end, value)
    
    def connect_id(self, start: int, end: int, value: str):
        self.graph.connect_id(start, end, value)
    
    def __str__(self):
        res = ""
        for id1, node1 in self.graph.gen_node_id():
            for id2, node2 in self.graph.gen_node_id():
                if (id1, id2) in self.graph.edges:
                    res += f"{id1}<I: {node1.initial}, F: {node1.final}>"
                    res += f" ---> {self.graph.edges[(id1, id2)]} ---> "
                    res += f"{id2}<I: {node2.initial}, F: {node2.final}>\n"
        return res
