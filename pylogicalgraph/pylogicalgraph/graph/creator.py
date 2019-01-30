# -*- coding: utf-8 -*-
from .graphviz import GraphvizCreator

class GraphCreator:
    def __init__(self, format='png', params={}):
        self.params = params
        self.module = GraphvizCreator(format=format)

    def write(self, filename):
        self.module.write(filename)

    def graph(self):
        return self.module.graph()

    def subgraph(self, g, subgraph_name):
        return self.module.subgraph(g, subgraph_name)
