# -*- coding: utf-8 -*-
from .node import LogicNode

class LogicPlug:
    def __init__(self, plug_id="", name="", node=LogicNode()):
        self._plug_id = plug_id
        self._name = name
        self._node = node
    def __str__(self):
        return "{0}_{1}".format(self._plug_id, self._name)
    def __repr__(self):
        return "{0}_{1}".format(self._plug_id, self._name)
    @property
    def plug_id(self):
        return self._plug_id
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @property
    def node(self):
        return self._node
    @property
    def plug(self):
        return (self._plug_id, self._name)
