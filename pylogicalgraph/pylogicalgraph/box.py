# -*- coding: utf-8 -*-
# from .logic.box import LogicOperation, LogicBox
from .block import LogicalGraphBlock
from .logic.plug import LogicPlug

class LogicOperation:
    Ent = "Ent"
    Sum = "Sum"
    Prod = "Prod"
    Comp = "Comp"
    Lambda = "Lambda"
    Up = "Up"

class LogicalGraphBox:
    def __init__(self,
                 box_id,
                 box_type=LogicOperation.Ent,
                 box_list=[],
                 in_list=[],
                 out_list=[],
                 edge_list=[],
                 lambda_list=[],
                 up_list=[]):
        self._id_name = box_id
        self._box_type = box_type
        self._box_list = box_list
        self._in_list = in_list
        self._out_list = out_list
        self._edge_list = edge_list
        self._lambda_list = lambda_list
        self._up_list = up_list

    @property
    def id_name(self):
        return self._id_name
    @property
    def box_type(self):
        return self._box_type
    @property
    def box_list(self):
        return self._box_list
    @property
    def in_list(self):
        return self._in_list
    @property
    def out_list(self):
        return self._out_list
    @property
    def edge_list(self):
        return self._edge_list
    @property
    def lambda_list(self):
        return self._lambda_list
    @property
    def up_list(self):
        return self._up_list
    @property
    def rank(self):
        rank = -1
        if self._box_type == LogicOperation.Ent:
            rank = 0
        elif self._box_type == LogicOperation.Sum:
            rank = max(self._box_list[0].rank, self._box_list[1].rank) + 1
        elif self._box_type == LogicOperation.Prod:
            rank = max(self._box_list[0].rank, self._box_list[1].rank) + 1
        elif self._box_type == LogicOperation.Comp:
            rank = max(self._box_list[0].rank, self._box_list[1].rank) + 1
        elif self._box_type == LogicOperation.Lambda:
            rank = self._box_list[0].rank + 1
        elif self._box_type == LogicOperation.Up:
            rank = self._box_list[0].rank + 1
        else:
            rank = -1
        return rank
    @property
    def shape(self):
        columns = 0
        rows = 0
        if self._box_type == LogicOperation.Ent:
            columns = 1
            rows = 1
        elif self._box_type == LogicOperation.Sum:
            columns = self._box_list[0].columns + self._box_list[1].columns
            rows = max(self._box_list[0].rows, self._box_list[1].rows)
        elif self._box_type == LogicOperation.Prod:
            columns = self._box_list[0].columns + self._box_list[1].columns
            rows = max(self._box_list[0].rows, self._box_list[1].rows)
        elif self._box_type == LogicOperation.Comp:
            columns = max(self._box_list[0].columns, self._box_list[1].columns)
            rows = self._box_list[0].rows + self._box_list[1].rows
        elif self._box_type == LogicOperation.Lambda:
            columns = self._box_list[0].columns
            rows = self._box_list[0].rows
        elif self._box_type == LogicOperation.Up:
            columns = self._box_list[0].columns
            rows = self._box_list[0].rows
        else:
            columns = 0
            rows = 0
        return (columns, rows)
    @property
    def columns(self):
        return self.shape[0]
    @property
    def rows(self):
        return self.shape[1]

    def get_box_color(self):
        ret_color = "white"
        if self.box_type == LogicOperation.Ent:
            ret_color = "white"
        elif self.box_type == LogicOperation.Sum:
            # ret_color = "antiquewhite"
            # ret_color = "lightgray"
            # ret_color = "ghostwhite"
            # ret_color = "snow"
            # ret_color = "green"
            ret_color = "darkgreen"
        elif self.box_type == LogicOperation.Prod:
            ret_color = "pink"
            # ret_color = "salmon"
            # ret_color = "violet"
        elif self.box_type == LogicOperation.Comp:
            # ret_color = "blue"
            ret_color = "cornflowerblue"
        elif self.box_type == LogicOperation.Lambda:
            ret_color = "white"
        elif self.box_type == LogicOperation.Up:
            ret_color = "white"
        else:
            ret_color = "black"
        return ret_color

    def dump(self):
        print("box {0} type   = {1}".format(self._id_name, self._box_type))
        print("box {0} in     = {1}".format(self._id_name, self.in_list))
        print("box {0} out    = {1}".format(self._id_name, self.out_list))
        print("box {0} edge   = {1}".format(self._id_name, self.edge_list))
        print("box {0} lambda = {1}".format(self._id_name, self.lambda_list))
        print("box {0} up     = {1}".format(self._id_name, self._up_list))
        print("box {0} rank    = {1}".format(self._id_name, self.rank))
        print("box {0} columns = {1}".format(self._id_name, self.columns))
        print("box {0} rows    = {1}".format(self._id_name, self.rows))

    def DeepCopy(self):
        new_lbox = LogicalGraphBox(self._id_name,
                                   box_type=self._box_type,
                                   box_list=list(self._box_list),
                                   in_list=list(self._in_list),
                                   out_list=list(self._out_list),
                                   edge_list=list(self._edge_list),
                                   lambda_list=list(self._lambda_list),
                                   up_list=list(self._up_list))
        return new_lbox

    def set_plugs(self, target_node, mod_dict):
        for k in mod_dict.keys():
            for i in range(len(self._in_list)):
                plug = self._in_list[i]
                if (plug.node.node_id == target_node.node_id) and (plug.name == k):
                    self._in_list[i].name = mod_dict[k]
            for i in range(len(self._out_list)):
                plug = self._out_list[i]
                if (plug.node.node_id == target_node.node_id) and (plug.name == k):
                    self._out_list[i].name = mod_dict[k]

    @classmethod
    def Ent(cls, box_id, node_kind="", in_list=[], out_list=[]):
        ret = 0

        id_name = "{0}_0".format(box_id)
        block = LogicalGraphBlock(id_name, node_kind, in_list, out_list)

        lbox = LogicalGraphBox(box_id,
                               box_type=LogicOperation.Ent,
                               box_list=[block],
                               in_list=block.in_list,
                               out_list=block.out_list)
        return ret, lbox

    @classmethod
    def Sum(cls, box_id, lbox_1, lbox_2):
        ret = 0
        lbox = LogicalGraphBox(box_id,
                               box_type=LogicOperation.Sum,
                               box_list=[lbox_1, lbox_2],
                               in_list=(lbox_1.in_list + lbox_2.in_list),
                               out_list=(lbox_1.out_list + lbox_2.out_list),
                               edge_list=(lbox_1.edge_list + lbox_2.edge_list),
                               lambda_list=(lbox_1.lambda_list + lbox_2.lambda_list),
                               up_list=(lbox_1.up_list + lbox_2.up_list))
        return ret, lbox

    @classmethod
    def Prod(cls, box_id, lbox_1, lbox_2):
        ret = 0
        lbox = LogicalGraphBox(box_id,
                               box_type=LogicOperation.Prod,
                               box_list=[lbox_1, lbox_2],
                               in_list=(lbox_1.in_list + lbox_2.in_list),
                               out_list=(lbox_1.out_list + lbox_2.out_list),
                               edge_list=(lbox_1.edge_list + lbox_2.edge_list),
                               lambda_list=(lbox_1.lambda_list + lbox_2.lambda_list),
                               up_list=(lbox_1.up_list + lbox_2.up_list))
        return ret, lbox

    @classmethod
    def Comp(cls, box_id, lbox_1, lbox_2):
        ret = 0
        print("out_list = {}".format(lbox_2.out_list))
        new_edge_list = lbox_1.edge_list + lbox_2.edge_list
        ret = LogicalGraphBox.Comp_box(lbox_1, lbox_2, new_edge_list)
        lbox = LogicalGraphBox(box_id,
                               box_type=LogicOperation.Comp,
                               box_list=[lbox_1, lbox_2],
                               in_list=lbox_1.in_list,
                               out_list=lbox_2.out_list,
                               edge_list=new_edge_list,
                               lambda_list=(lbox_1.lambda_list + lbox_2.lambda_list),
                               up_list=(lbox_1.up_list + lbox_2.up_list))
        print("out_list = {}".format(lbox_2.out_list))
        return ret, lbox

    @classmethod
    def Comp_box(cls, lbox_1, lbox_2, edge_list):
        out_list = lbox_1.out_list
        in_list = lbox_2.in_list
        if len(out_list) != len(in_list):
            ret = -1
            return ret

        num_of_plugs = len(out_list)
        for i in range(num_of_plugs):
            plug_out = out_list[i]
            plug_in = in_list[i]
            if plug_in.name != 'X' and plug_in.name != 'Y' and not (plug_out.name == plug_in.name):
                print("plug_in name = {}".format(plug_in.name))
                print("plug_out name = {}".format(plug_out.name))
                ret = -2
                return ret

        for i in range(num_of_plugs):
            plug_out = out_list[i]
            plug_in = in_list[i]
            if plug_in.name == 'X' or plug_in.name == 'Y':
                print("set plug_out name = {}".format(plug_out.name))
                print("set plug_in name = {}".format(plug_in.name))
                lbox_2.dump()
                lbox_2.set_plugs(plug_in.node, {plug_in.name:plug_out.name})
                lbox_2.dump()

        out_list = lbox_1.out_list
        in_list = lbox_2.in_list

        new_edge_list = []
        for i in range(num_of_plugs):
            plug_out = out_list[i]
            plug_in = in_list[i]
            new_edge_list.append((plug_out.node, plug_in.node))
        edge_list.extend(new_edge_list)

    @classmethod
    def Lamb(cls, box_id, target_lbox, in_plug_id, out_plug_id):
        ret = 0
        in_plug_list = [p for p in target_lbox.in_list if p.plug_id == in_plug_id]
        out_plug_list = [p for p in target_lbox.out_list if p.plug_id == out_plug_id]

        if (len(in_plug_list) != 1) or (len(out_plug_list) != 1):
            ret = -1
            return ret, LogicalGraphBox(box_id)

        lambda_list = target_lbox.lambda_list
        lambda_list.append((in_plug_list[0], out_plug_list[0]))
        print("lambda_list = {}".format(lambda_list))

        lbox = LogicalGraphBox(box_id,
                               box_type=LogicOperation.Lambda,
                               box_list=[target_lbox],
                               in_list=target_lbox.in_list,
                               out_list=target_lbox.out_list,
                               edge_list=target_lbox.edge_list,
                               lambda_list=lambda_list,
                               up_list=target_lbox.up_list)
        return ret, lbox

    @classmethod
    def Up(cls, id_name, target_lbox, in_plug):
        ret = 0
        up_list = target_lbox.up_list
        up_list.append(LogicPlug(node_id=in_plug[0], name=in_plug[1]))
        lbox = LogicalGraphBox(box_id,
                               box_type=LogicOperation.Up,
                               box_list=[lbox_1, lbox_2],
                               in_list=target_lbox.in_list,
                               out_list=target_lbox.out_list,
                               edge_list=target_lbox.edge_list,
                               lambda_list=target_lbox.lambda_list,
                               up_list=up_list)
        return ret, lbox

    def draw_graph(self, creator, graph, prefix=''):
        inputs = self.in_list
        outputs = self.out_list
        print("in_list type  = {}".format(type(inputs)))
        print("out_list type = {}".format(type(outputs)))
        print("in_list  = {}".format(inputs))
        print("out_list = {}".format(outputs))

        # plug & subgraph
        graph.attr('node', shape='box')
        for elm in inputs:
            # graph.node("{}_in_{}".format(prefix, elm), label="{0}".format(elm))
            graph.node("{}_in_{}".format(prefix, elm))

        # for lbox in self._box_list:
        #     lbox.draw(creator, graph, prefix=prefix)

        color_name = self.get_box_color()
        subgraph_name = "cluster_{0}_{1}".format(prefix, self.id_name)
        with graph.subgraph(name=subgraph_name) as subgraph:
            subgraph.attr(style='filled')
            subgraph.attr(color=color_name)
            for lbox in self._box_list:
                lbox.draw(creator, subgraph, prefix=prefix)

        graph.attr('node', shape='box')
        for elm in outputs:
            # graph.node("{}_out_{}".format(prefix, elm), label="{0}".format(elm))
            graph.node("{}_out_{}".format(prefix, elm))

        # Edge
        for elm in inputs:
            # graph.edge("{}_in_{}".format(prefix, elm), "{}_{}".format(prefix, elm.node), label="{0}".format(elm))
            graph.edge("{}_in_{}".format(prefix, elm), "{}_{}".format(prefix, elm.node))

        for elm in outputs:
            # graph.edge("{}_{}".format(prefix, elm), "{}_out_{}".format(prefix, elm.node), label="{0}".format(elm))
            graph.edge("{}_{}".format(prefix, elm.node), "{}_out_{}".format(prefix, elm))

        for elm in self.edge_list:
            # graph.edge("{}_{}".format(prefix, elm[0]), "{}_{}".format(prefix, elm[1]), label=elm[0][1], arrowtail=None)
            graph.edge("{}_{}".format(prefix, elm[0]), "{}_{}".format(prefix, elm[1]))

        for elm in self.lambda_list:
            # graph.edge("{}_in_{}".format(prefix, elm), "{}_{}".format(prefix, elm.node), label="{0}".format(elm))
            src_name = "{}_in_{}".format(prefix, elm[0])
            dst_name = "{}_out_{}".format(prefix, elm[1])
            # graph.edge(src_name, dst_name, dir="back")
            graph.edge(src_name, dst_name, dir="back", tailport="n", headport="s")

    def draw(self, creator, graph, prefix=''):
        color_name = self.get_box_color()
        subgraph_name = "cluster_{0}_{1}".format(prefix, self.id_name)
        with graph.subgraph(name=subgraph_name) as c:
            c.attr(style='filled')
            c.attr(color=color_name)
            for lbox in self._box_list:
                lbox.draw(creator, c, prefix=prefix)
