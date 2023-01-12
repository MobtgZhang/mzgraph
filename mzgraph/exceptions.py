class MzGraphError(Exception):
    """Root exception class for all library exceptions. Only used for subclassing."""
    pass

class NonexistentNodeError(MzGraphError):
    """Thrown when a node does not exist within a graph."""
    def __init__(self, node_id):
        self.node_id = node_id

    def __str__(self):
        return 'Node "{}" does not exist.'.format(self.node_id)


class NonexistentEdgeError(MzGraphError):
    """Thrown when an edge does not exist within a graph."""
    def __init__(self, edge_id):
        self.edge_id = edge_id

    def __str__(self):
        return 'Edge "{}" does not exist.'.format(self.edge_id)
