from graph import Graph
import graphviz

class FSM:
    def __init__(self, graph: Graph, initials=None, finals=None):
        self.graph = graph
        self.initials = set() if initials is None else initials
        self.finals = set() if finals is None else finals
    
    def get_nodes(self):
        return self.graph.nodes
    
    def get_table(self):
        return self.graph.table
    
    def get_initials(self):
        return self.initials
    
    def get_finals(self):
        return self.finals
    
    def set_initial(self, node):
        if node not in self.get_nodes():
            self.add_node(node)
        self.initials.add(node)
    
    def set_final(self, node):
        if node not in self.get_nodes():
            self.add_node(node)
        self.finals.add(node)
    
    def remove_initial(self, node):
        initials = self.get_initials()
        if node in initials:
            initials.remove(node)
    
    def remove_final(self, node):
        finals = self.get_finals()
        if node in finals:
            finals.remove(node)
    
    def add_sub_set(self, node, initial, final):
        if initial: self.set_initial(node)
        if final:   self.set_final(node)
    
    def add_node(self, node, initial=False, final=False):
        self.add_sub_set(node, initial, final)
        self.graph.add_node()
    
    def connect(self, src, dest, value, src_i=False, src_f=False, dest_i=False, dest_f=False):
        self.add_node(src, src_i, src_f)
        self.add_node(dest, dest_i, dest_f)
        self.graph.connect(src, dest, value)
    
    def deconnect(self, src, dest):
        self.graph.deconnect(src, dest)
    
    def remove_node(self, node):
        self.remove_initial(node)
        self.remove_final(node)
        self.graph.remove_node(node)
        
    def render(self, format='png', keep_source=False):
        initials = self.get_initials()
        finals = self.get_finals()
        table = self.get_table()
        nodes = self.get_nodes()
        
        f = graphviz.Digraph('automaton')
        f.attr(rankdir='LR', size="8,5")
        
        # arrow for initials states
        for node in initials:
            f.attr('node', shape='point')
            f.node(f'qi{node}')
        
        # finals states
        for node in nodes:
            if node in finals:
                f.attr('node', shape='doublecircle')
                f.node(f'{node}')
            else:
                f.attr('node', shape='circle')
                f.node(f'{node}')
            if node in initials:
                f.edge(f'qi{node}', f'{node}')
        
        # states
        f.attr('node', shape='circle')
        for src, dest in table:
            f.edge(f'{src}', f'{dest}', label=",".join(sorted(list(table[(src, dest)]))))
        
        f.render(format=format, cleanup=not keep_source)
    
    def is_node_accessible(self, node):
        if node in self.get_initials():
            return True
        for init in self.get_initials():
            if self.graph.exists_path(init, node):
                return True
        return False
    
    def is_accessible(self):
        for node in self.get_nodes():
            if not self.is_node_accessible(node):
                return False
        return True
    
    def is_node_coaccessible(self, node):
        if node in self.get_finals():
            return True
        for final in self.get_finals():
            if self.graph.exists_path(node, final):
                return True
        return False
    
    def is_coaccessible(self):
        for node in self.get_nodes():
            if not self.is_node_coaccessible(node):
                return False
        return True

def create_fsm(table: list[tuple[int, int, str]], initials: set[int], finals: set[int]):
    graph = Graph()
    for src, dest, value in table:
        graph.connect(src, dest, value)
    return FSM(graph, initials, finals)


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
    fsm1.render('pdf')
    
