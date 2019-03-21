import networkx as nx
import networkx.convert as convert


# Class "GraphQW" is a networkx graph with generated individual attributes
class GraphQW(nx.DiGraph):
    def __init__(self, g = {}, q = None, dq = None, limcoal = None, dw = None):
        self.graph = {}
        self._node = self.node_dict_factory()
        self._adj = self.adjlist_outer_dict_factory()  # empty adjacency dict
        self._pred = self.adjlist_outer_dict_factory()  # predecessor
        self._succ = self._adj  # successor
        if g is not None:
            convert.to_networkx_graph(g, create_using=self)
            nx.set_node_attributes(self, name='indeg', values=dict(self.in_degree(weight='weight')))
            self.set_quota(q, dq)
            self.set_size(dw)
            self.coal = limcoal
            for edge in self.edges(data = True):
                if 'weight' not in edge[2]:
                    self.set_edge_attr('weight', 1)
                break


    def set_edge_attr(self, name, value):
        edges = self.edges()
        edge_list = dict(zip(edges, [value] * len(edges)))
        nx.set_edge_attributes(self, edge_list, name)

    def set_size(self, dw):
        if dw is None:
            pp = self.out_degree(weight='weight')
            nx.set_node_attributes(self, name='size', values=dict(self.out_degree(weight='weight')))
        else:
            self.set_param('size', dw)

    def set_quota(self, q, dq):
        if dq is None:
            ql = dict()
            d = self.in_degree(weight='weight')
            for x, y in d:
                ql[x] = y * q / 100
            nx.set_node_attributes(self, name='q', values=ql)
        else:
            self.set_param('q', dq)

    def set_param(self, name, data):
        if data is not None:
            if isinstance(data, dict):
                nx.set_node_attributes(self, name=name, values=data)
            elif isinstance(data, list):
                if len(self.nodes()) == len(data):
                    nx.set_node_attributes(self, name=name, values=dict(zip(self.nodes(), data)))
            elif isinstance(data, float) or isinstance(data, int):
                nx.set_node_attributes(self, name=name, values=dict(zip(self.nodes(), [data] * len(self.nodes()))))

    def aggregate(self, name=''):
        pers = dict(zip(self.nodes(), [0] * len(self)))
        for edge in self.edges(data=True):
            pers[edge[0]] += self.node[edge[1]]['size']*edge[2]['weight']
        pers = self.normalize(pers)
        self.set_param(name, pers)
        return pers

    @staticmethod
    def normalize(arr):
        s = sum(arr.values())
        for el in arr:
            arr[el] /= s
        return arr
