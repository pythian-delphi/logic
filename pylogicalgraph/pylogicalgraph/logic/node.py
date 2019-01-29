# -*- coding: utf-8 -*-
class LogicNode:
    def __init__(self, node_id="", node_type=""):
        self._node_id = node_id
        self._node_type = node_type
    def __str__(self):
        return "{0}_{1}".format(self._node_id, self._node_type)
    def __repr__(self):
        return "{0}_{1}".format(self._node_id, self._node_type)
    @property
    def node_id(self):
        return self._node_id
    @property
    def node_type(self):
        return self._node_type
    @property
    def node(self):
        return (self._node_id, self._node_type)
