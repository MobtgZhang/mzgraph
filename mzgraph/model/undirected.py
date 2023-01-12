import copy
from ..exceptions import NonexistentEdgeError,NonexistentNodeError
from .directed import DiGraph
class UnDiGraph(DiGraph):
    def __deepcopy__(self,memo=None):
        graph = UnDiGraph()
        graph.nodes = copy.deepcopy(self.nodes)
        graph.edges = copy.deepcopy(self.edges)
        graph.next_edge_id = self.next_edge_id
        graph.next_node_id = self.next_node_id
        graph._num_edges = self._num_edges
        graph._num_nodes = self._num_nodes
        return graph
    def add_edge(self, node_a, node_b, cost=1, **attr):
        edge_id = super(UnDiGraph,self).add_edge(node_a,node_b,cost)
        self.nodes[node_b]["edges"].append(edge_id)
        return edge_id
    def neighbors(self, node_id):
        node = self.get_node(node_id)
        flattened_nodes_list = []
        for a,b in [self.get_edge(edge_id)["edge"] for edge_id in node["edges"]]:
            flattened_nodes_list.append(a)
            flattened_nodes_list.append(b)
        node_set = set(flattened_nodes_list)
        if node_id in node_set:
            node_set.remove(node_id)
        return [nid for nid in node_set]
    def processors(self, node_id):
        return self.neighbors(node_id)
    def delete_edge_by_id(self, edge_id):
        edge = self.get_edge(edge_id)

        from_node_id = edge['edge'][0]
        from_node = self.get_node(from_node_id)

        from_node['edges'].remove(edge_id)

        to_node_id = edge['edge'][1]
        to_node = self.get_node(to_node_id)

        to_node['edges'].remove(edge_id)

        del self.edges[edge_id]

        self._num_edges -= 1

    def move_edge_target(self, edge_id, node_a):
        edge = self.get_edge(edge_id)

        original_target_node_id = edge['edge'][1]
        original_target_node = self.get_node(original_target_node_id)
        original_target_node['edges'].remove(edge_id)

        new_target_node_id = node_a
        new_target_node = self.get_node(new_target_node_id)
        new_target_node['edges'].append(edge_id)

        edge['edge'] = (edge['edge'][0], node_a)
    def move_edge_source(self, edge_id, node_a):
        return self.move_edge_target(edge_id,node_a)
    