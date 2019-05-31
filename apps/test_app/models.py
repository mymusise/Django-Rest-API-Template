from django.db import models
from datetime import datetime
import numpy as np


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(phi * np.pi / 360)
    y = rho * np.sin(phi * np.pi / 360)
    return [round(x, 2), round(y, 2)]


class GraphConfigMixin(object):
    netword = []
    nodes_map = {}
    r = 1.3
    angel = 180

    def build_coord(self, tree):
        for level, nodes in enumerate(tree):
            n = len(nodes)
            offset = self.angel / 2 
            phi = self.angel / (n + 1)
            for i, node in enumerate(nodes):
                node.coord = [level * self.r, phi * (i + 1) + offset]

    def get_nodes(self, tree):
        for nodes in tree:
            for node in nodes:
                yield {
                    'kid': node.to_id,
                    'name': self.nodes_map[node.to_id],
                    'value': list(pol2cart(*node.coord))
                }

    def get_edges(self, tree):
        for edge in self.edges:
            if edge.from_id < 0:
                    continue
            yield {
                'source': self.nodes_map[edge.from_id],
                'target': self.nodes_map[edge.to_id]
            }

    def get_data(self):
        tree = self.netword
        self.build_coord(tree)
        nodes = list(self.get_nodes(tree))
        edges = list(self.get_edges(tree))
        return {
            'nodes': nodes,
            'edges': edges,
        }


class Knowledge(models.Model):
    name = models.CharField(max_length=32)
    create_at = models.DateTimeField(default=datetime.now)


class Graph(models.Model, GraphConfigMixin):
    name = models.CharField(max_length=32)
    user_id = models.IntegerField(default=0)  # should not None
    create_at = models.DateTimeField(default=datetime.now)

    @property
    def _root(self):
        return GraphEdge(from_id=-1, to_id=0, graph_id=self.id)

    @property
    def _roots(self):
        return list(filter(lambda x: x.from_id == 0, self.edges))

    def make_tree(self):
        self.tree = [[self._root]]
        ids = [root.to_id for root in self.tree[0]]
        nexts = list(filter(lambda x: x.from_id in ids, self.edges))
        nexts = sorted(nexts, key=lambda x: (x.from_id, x.to_id))
        if nexts:
            self.tree.append(nexts)
        while nexts:
            ids = [n.to_id for n in nexts]
            nexts = list(filter(lambda x: x.from_id in ids, self.edges))
            nexts = sorted(nexts, key=lambda x: (x.from_id, x.to_id))
            if nexts:
                self.tree.append(nexts)

    @property
    def netword(self):
        self.edges = list(GraphEdge.objects.filter(graph_id=self.id))
        self.nodes = list(Knowledge.objects.filter(
            id__in=list(set([e.to_id for e in self.edges]))))
        self.nodes_map = dict([(0, self.name)] + [(n.id, n.name)
                                                  for n in self.nodes])
        self.make_tree()
        return self.tree


class GraphEdge(models.Model):
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    graph_id = models.IntegerField()
    create_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.graph_id}: {self.from_id} -> {self.to_id}"
