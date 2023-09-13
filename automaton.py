from graph import Graph, Node
import graphviz

class NodeNotExists(Exception):
    pass

class RFSM:
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

    def remove_node(self, node: int | Node):
        if isinstance(node, int):
            node = self.graph.get_node(node)
        self.remove_node_sub_set(node)
        self.graph.remove_node(node)

    def connect(self, start: int | Node, end: int | Node, value: str):
        if isinstance(start, Node):
            self.add_sub_set(start)
        if isinstance(end, Node):
            self.add_sub_set(end)
        self.graph.connect(start, end, value)

    def deconnect(self, start: int | Node, end: int | Node):
        self.graph.deconnect(start, end)

    def __str__(self):
        res = "Nodes : \n"
        for id, node in self.graph.gen_node_id():
            res += f"id: {id} <I: {node.initial}, F: {node.final}>\n"
        res += "\nConnections :\n"
        for id1 in self.graph.gen_id():
            for id2 in self.graph.gen_id():
                if (id1, id2) in self.graph.edges:
                    res += f"{id1} --> {self.graph.edges[(id1, id2)]} --> {id2}\n"
        return res

    def exist_path(self, start: int | Node, end: int | Node):
        return self.graph.exist_path(start, end)

    def to_dot(self, name: str):
        with open(name + ".dot", "w") as f:
            f.write("digraph finite_state_machine {\n")
            f.write("\trankdir=LR;\n")
            f.write('\tsize="8,5"\n\n')

            # draw arrow for initials states
            for node in self.initials:
                f.write(f"\tnode [shape = point] qi{node.id};\n")

            # draw states
            for id in self.graph.node_table:
                if self.graph.get_node(id) in self.finals:
                    f.write(f'\tnode [shape = doublecircle, label="{id}"] q{id};\n')
                else:
                    f.write(f'\tnode [shape = circle, label="{id}"] q{id};\n')
                if self.graph.get_node(id) in self.initials:
                    # draw link between the arrow and the node
                    f.write(f"\tqi{id} -> q{id}\n")

            # draw connections
            for start, end in self.graph.edges:
                label = ",".join(sorted(list(self.graph.edges[(start, end)])))
                f.write(f'\tq{start} -> q{end} [label="{label}"];\n')

            # footer
            f.write("}")

    def to_png(self, name: str):
        self.to_dot(name)
        graphviz.render("dot", "png", name + ".dot", outfile=name + ".png")


class FiniteStateMachine(RFSM):
    def __init__(self, graph: Graph):
        super().__init__(graph)

    def cast_to_node(func):
        def cast(self, node):
            if isinstance(node, int):
                node = self.graph.get_node(node)
                if node is None:
                    raise NodeNotExists
            return func(self, node)
        return cast
    
    @cast_to_node
    def is_node_accessible(self, node: int | Node):
        for n in self.initials:
            if self.exist_path(n, node):
                return True
        return False

    @cast_to_node
    def is_node_coaccessible(self, node: int | Node):
        for n in self.finals:
            if self.exist_path(node, n):
                return True
        return False

def create_fsm(table: list[tuple[int, int, str]], init: set[int], final: set[int]):
    graph = Graph()
    nodes = {}
    for start, end, value in table:
        if start not in nodes:
            nodes[start] = Node(start in init, start in final)
        if end not in nodes:
            nodes[end] = Node(end in init, end in final)
        graph.connect(nodes[start], nodes[end], value)
    return FiniteStateMachine(graph)


if __name__ == "__main__":
    fsm1 = create_fsm(
        [
            (0, 3, 'b'),
            (0, 1, 'b'),
            (1, 2, 'a'),
            (1, 2, 'b'),
            (2, 1, 'a'),
            (2, 1, 'b'),
            (2, 3, 'b'),
            (4, 4, 'a'),
            (4, 4, 'b'),
            (4, 3, 'a'),
        ],
        {0, 4},
        {4},
    )
    print(fsm1)
    print(fsm1.is_node_accessible(4))
