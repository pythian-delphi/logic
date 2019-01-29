# -*- coding: utf-8 -*-
from .box import LogicalGraphBox
from .graph import GraphCreator

class LogicalGraphCanvas:
    def __init__(self, params={}):
        self.params = params
        self.count = 0
        self.lbox_dict = {}
        self.history_dict = {}

    def __get_BoxID(self):
        # box_id = "Box_#{}".format(self.count)
        box_id = "#{}".format(self.count)
        self.count += 1
        return box_id

    def get_logic_box(self, lbox_id):
        return self.lbox_dict[lbox_id]

    def Ent(self, node_type='', in_list=[], out_list=[]):
        ret = 0
        id_name = self.__get_BoxID()
        ret, lbox = LogicalGraphBox.Ent(id_name, node_type, in_list, out_list)

        self.lbox_dict[id_name] = lbox
        self.history_dict[id_name] = ("Ent",[])
        return ret,id_name

    def Prod(self, lbox_id_1, lbox_id_2):
        ret = 0
        lbox_1 = self.lbox_dict[lbox_id_1].DeepCopy()
        lbox_2 = self.lbox_dict[lbox_id_2].DeepCopy()

        id_name = self.__get_BoxID()
        ret, lbox = LogicalGraphBox.Prod(id_name, lbox_1, lbox_2)

        self.lbox_dict[id_name] = lbox
        self.history_dict[id_name] = ("Prod",[lbox_id_1, lbox_id_2])
        return ret,id_name

    def Sum(self, lbox_id_1, lbox_id_2):
        ret = 0
        lbox_1 = self.lbox_dict[lbox_id_1].DeepCopy()
        lbox_2 = self.lbox_dict[lbox_id_2].DeepCopy()

        id_name = self.__get_BoxID()
        ret, lbox = LogicalGraphBox.Sum(id_name, lbox_1, lbox_2)

        self.lbox_dict[id_name] = lbox
        self.history_dict[id_name] = ("Sum",[lbox_id_1, lbox_id_2])
        return ret,id_name

    def Comp(self, lbox_id_1, lbox_id_2):
        ret = 0
        lbox_1 = self.lbox_dict[lbox_id_1].DeepCopy()
        lbox_2 = self.lbox_dict[lbox_id_2].DeepCopy()

        id_name = self.__get_BoxID()
        ret, lbox = LogicalGraphBox.Comp(id_name, lbox_1, lbox_2)

        self.lbox_dict[id_name] = lbox
        self.history_dict[id_name] = ("Comp",[lbox_id_1, lbox_id_2])
        return ret,id_name

    def Lamb(self, lbox_id_1, in_plug_1, in_plug_2):
        ret = 0
        lbox_1 = self.lbox_dict[lbox_id_1].DeepCopy()

        id_name = self.__get_BoxID()
        ret, lbox = LogicalGraphBox.Lamb(id_name, lbox_1, in_plug_1, in_plug_2)

        self.lbox_dict[id_name] = lbox
        self.history_dict[id_name] = ("Lamb",[lbox_id_1])
        return ret,id_name

    def Up(self, lbox_id_1, in_plug):
        ret = 0
        lbox_1 = self.lbox_dict[lbox_id_1].DeepCopy()

        id_name = self.__get_BoxID()
        ret, lbox = LogicalGraphBox.Up(id_name, lbox_1, in_plug)

        self.lbox_dict[id_name] = lbox
        self.history_dict[id_name] = ("Up",[lbox_id_1])
        return ret,id_name

    def draw_box(self, lbox_id, filename):
        creator = GraphCreator()
        graph = creator.graph()
        # self.lbox_dict[lbox_id].draw(creator, graph, prefix=lbox_id)
        self.lbox_dict[lbox_id].draw_graph(creator, graph, prefix=lbox_id)
        creator.write(filename)
