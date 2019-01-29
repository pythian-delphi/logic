# -*- coding: utf-8 -*-
# from .logic.block import LogicBlock
from .logic.plug import LogicPlug
from .logic.node import LogicNode

class LogicalGraphBlock:
    def __init__(self, id_name, node_kind='', in_list=[], out_list=[]):
        self._id_name = id_name
        self._node_list  = [LogicNode(id_name, node_kind)]
        self._in_list = [LogicPlug("{}_{}".format(id_name,i), n, LogicNode(id_name, node_kind)) for i,n in enumerate(in_list)]
        self._out_list = [LogicPlug("{}_{}".format(id_name,i), n, LogicNode(id_name, node_kind)) for i,n in enumerate(out_list)]
        self._edge_list = []
        self._lambda_list = []
        self._up_list = []

    @property
    def id_name(self):
        return self._id_name
    @property
    def node_list(self):
        return self._node_list
    @property
    def in_list(self):
        return self._in_list
    @property
    def out_list(self):
        return self._out_list

    def draw(self, creator, g, prefix=''):
        # g.attr('node', shape='box')
        # for elm in self.in_list:
        #     g.node("{}_in_{}".format(prefix, elm), label="{0}".format(elm))

        g.attr('node', shape='ellipse')
        for elm in self.node_list:
            # g.node("{}_{}".format(prefix, elm), label="{0}".format(elm))
            g.node("{}_{}".format(prefix, elm))

        # g.attr('node', shape='box')
        # for elm in self.out_list:
        #     g.node("{}_out_{}".format(prefix, elm), label="{0}".format(elm))
