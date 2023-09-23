class Graph:
    def __init__(self):
        self.nodes = set()
        self.table = {}

    def add_node(self, node):
        if node in self.nodes:
            return
        self.nodes.add(node)

    def connect(self, src, dest, value):
        self.add_node(src)
        self.add_node(dest)

        if (src, dest) in self.table:
            self.table[(src, dest)].add(value)
        else:
            self.table[(src, dest)] = {value}

    def remove_node(self, node):
        if node in self.nodes:
            to_del = set()
            for couple in self.table:
                if node in couple:
                    to_del.add(couple)
            for couple in to_del:
                self.deconnect(*couple)
            self.nodes.remove(node)
    
    def get_neighbours(self, node):
        for src, dest in self.table:
            if src == node:
                yield dest

    def deconnect(self, src, dest):
        if (src, dest) in self.table:
            self.table.pop((src, dest))

    def exists_path(self, src, dest, done=None):
        if done is None:
            done = set()
        if src == dest:
            return True
        
        done.add(src)
        for node in self.get_neighbours(src):
            if self.exists_path(node, dest, done):
                return True
        return False
        
