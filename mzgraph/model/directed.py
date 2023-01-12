import copy
from ..exceptions import NonexistentEdgeError,NonexistentNodeError

class DiGraph:
    nodes = None
    edges = None
    next_node_id = 1
    next_edge_id = 1
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self._num_edges = 0
        self._num_nodes = 0
    def __deepcopy__(self,memo=None):
        graph = DiGraph()
        graph.nodes = copy.deepcopy(self.nodes)
        graph.edges = copy.deepcopy(self.edges)
        graph.next_node_id = self.next_node_id
        graph.next_edge_id = self.next_edge_id
        graph._num_edges = self._num_edges
        graph._num_nodes = self._num_nodes
        return graph
    def num_nodes(self):
        return self._num_edges
    def num_edges(self):
        return self._num_edges
    def generate_node_id(self):
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id
    def generate_edge_id(self):
        edge_id = self.next_edge_id
        self.next_edge_id += 1
        return edge_id
    def add_node(self,**attr):
        node_id = self.generate_node_id()
        node = {
            "id":node_id,
            "edges":[],
            "data":{}
        }
        node["data"].upate(attr)
        self.nodes[node_id] = node
        self._num_nodes += 1
        return node_id
    def add_edge(self,node_a,node_b,cost=1.0,**attr):
        try:
            self.nodes[node_a]
        except KeyError:
            raise NonexistentNodeError(node_a)
        try:
            self.nodes[node_b]
        except KeyError:
            NonexistentNodeError(node_b)
        # here create the new edge
        edge_id = self.generate_edge_id()
        edge = {
            "cost":cost,
            'id':edge_id,
            "edge":(node_a,node_b),
            "data":{}
        }
        edge["data"].update(attr)
        self.edges[edge_id] = edge
        self.nodes[node_a]['edges'].append(edge_id)
        self._num_edges += 1
        return edge_id
    def get_node(self,node_id):
        try:
            node_object = self.nodes[node_id]
        except KeyError:
            print("The node %s doesn't exists!"%str(node_id))
            return 
        return node_object
    def get_edge(self,edge_id):
        try:
            edge_object = self.edges[edge_id]
        except KeyError:
            print("The edge %s doesn't exists!"%str(edge_id))
            return 
        return edge_object
    def neighbors(self,node_id):
        node = self.get_node(node_id)
        return [self.get_edge(edge_id)['edge'][1] for edge_id in node['edges']]
    def processors(self,node_id):
        return [edge[0] for edge in self.edges if node_id==edge[1]]
    def has_edge(self,node_a,node_b):
        neighbors = self.neighbors(node_a)
        return node_b in neighbors
    def has_node(self,node):
        return node in self.nodes
    def edge_cost(self,node_a,node_b):
        cost = float('inf')
        node_obj_a = self.get_node(node_a)
        for edge_id in node_obj_a["edges"]:
            edge = self.get_edge(edge_id)
            edge_tmp = (node_a,node_b)
            if edge["edge"] == edge_tmp:
                cost = edge["cost"]
                break
        return cost
    @property
    def nodes(self):
        return list(self.nodes.keys())
    @property
    def edges(self):
        return list(self.edges.keys())
    @property
    def nodes_objs(self):
        return list(self.nodes.values())
    @property
    def edges_objs(self):
        return list(self.edges.values())
    def delete_edge_by_id(self,edge_id):
        edge = self.get_edge(edge_id)
        from_node_id = edge["edge"][0]
        from_node = self.get_node(from_node_id)
        from_node["edges"].remove(edge_id)
        del self.edges[edge_id]

        self._num_edges -= 1
    def delete_edge_by_node(self,node_a,node_b):
        node = self.get_node(node_a)

        edge_ids = []
        for e_id in node["edges"]:
            edge = self.get_edge(e_id)
            if edge["edge"][1] == node_b:
                edge_ids.append(e_id)
        # delete the edges

        for e in edge_ids:
            self.delete_edge_by_id(e)
    def delete_node(self,node_id):
        node = self.get_node(node_id)
        
        for e_id in node["edges"]:
            self.delete_edge_by_id(e_id)
        
        del self.nodes[node_id]

        self._num_nodes -= 1
    def move_edge_source(self,edge_id,node_a):
        edge = self.get_edge(edge_id)
        edge["edge"] = (node_a,edge["edge"][1])
        node_old = edge["edge"][0]
        # remove the edge from node_a
        node = self.get_node(node_old)
        node["edges"].remove(edge_id)
        # add the to node_b
        node = self.get_node(node_a)
        node["edges"].append(edge_id)
    def move_edge_target(self,edge_id,node_b):
        edge = self.get_edge(edge_id)
        # add the edge 
        edge["edge"] = (edge["edge"][0],node_b)
        
