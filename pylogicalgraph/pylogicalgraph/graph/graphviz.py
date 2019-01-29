# -*- coding: utf-8 -*-
from graphviz import Digraph

class GraphvizCreator:
    def __init__(self, format='png', params={}):
        self._params = params
        self._graph = Digraph('G', format=format)

    def write(self, filename):
        self._graph.render(filename)

    def graph(self):
        return self._graph

    def subgraph(self, g, subgraph_name):
        return g.subgraph(name=subgraph_name)

    def create_block_graph(self, lbox, g, prefix=None):
        if prefix is None:
            prefix = lbox.id_name

        g.attr('node', shape='box')
        for elm in lbox.in_list:
            g.node("{}_in_{}_{}".format(prefix, elm[0],elm[1]), label="{0} {1}".format(elm[0], elm[1]))

        g.attr('node', shape='ellipse')
        for elm in lbox.node_list:
            g.node("{}_{}".format(prefix, elm[0]), label="{0} {1}".format(elm[0], elm[1]))

        g.attr('node', shape='box')
        for elm in lbox.out_list:
            g.node("{}_out_{}_{}".format(prefix, elm[0],elm[1]), label="{0} {1}".format(elm[0], elm[1]))

        # Edge
        for elm in lbox.in_list:
            taget_id = elm[0]
            g.edge("{}_in_{}_{}".format(prefix, elm[0],elm[1]), "{}_{}".format(prefix, taget_id), label="{0} {1}".format(elm[0], elm[1]))

        for elm in lbox.out_list:
            taget_id = elm[0]
            g.edge("{}_{}".format(prefix, taget_id), "{}_out_{}_{}".format(prefix, elm[0],elm[1]), label="{0} {1}".format(elm[0], elm[1]))

        for elm in lbox.edge_list:
            g.edge("{}_{}".format(prefix, elm[0][0]), "{}_{}".format(prefix, elm[1][0]), label=elm[0][1], arrowtail=None)
