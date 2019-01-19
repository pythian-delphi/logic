# -*- coding: utf-8 -*-
from graphviz import Digraph

class LogicBlock:
    def __init__(self, id_name, node_list=[], in_list=[], out_list=[], edge_list=[]):
        self._block_id_name = id_name
        self._node_list  = node_list
        self._in_list = in_list
        self._out_list = out_list
        self._edge_list = edge_list
    def Ent_Node(self, node_id_name, node_type="", in_list=[], out_list=[]):
        self._node_list = [(node_id_name, node_type)]
        self._in_list = [(node_id_name, n) for n in in_list]
        self._out_list = [(node_id_name, n) for n in out_list]
        self._edge_list = []

    def search_node(self, id):
        for node in self._node_list:
            if id == node[0]:
                return node

    def DeepCopy(self):
        new_block = LogicBlock(
        self._block_id_name,
        node_list = list(self._node_list),
        in_list = list(self._in_list),
        out_list = list(self._out_list),
        edge_list = list(self._edge_list)
        )
        return new_block

    def dump(self):
        print("block {0} node = {1}".format(self._block_id_name, self._node_list))
        print("block {0} in   = {1}".format(self._block_id_name, self._in_list))
        print("block {0} out  = {1}".format(self._block_id_name, self._out_list))
        print("block {0} edge = {1}".format(self._block_id_name, self._edge_list))

    def create_graph(self, fname, format='png'):
        g = Digraph('G', format=format)
        self.create_block_graph(g)
        g.render(fname)

    def create_block_graph(self, g, prefix=None):
        if prefix is None:
            prefix = self._block_id_name

        g.attr('node', shape='box')
        for elm in self._in_list:
            g.node("{}_in_{}_{}".format(prefix, elm[0],elm[1]), label="{0} {1}".format(elm[0], elm[1]))

        g.attr('node', shape='ellipse')
        for elm in self._node_list:
            # g.node("{}_{}".format(elm[0],elm[1]))
            g.node("{}_{}".format(prefix, elm[0]), label="{0} {1}".format(elm[0], elm[1]))

        g.attr('node', shape='box')
        for elm in self._out_list:
            g.node("{}_out_{}_{}".format(prefix, elm[0],elm[1]), label="{0} {1}".format(elm[0], elm[1]))

        # Edge
        for elm in self._in_list:
            taget_id = elm[0]
            g.edge("{}_in_{}_{}".format(prefix, elm[0],elm[1]), "{}_{}".format(prefix, taget_id), label="{0} {1}".format(elm[0], elm[1]))

        for elm in self._out_list:
            taget_id = elm[0]
            g.edge("{}_{}".format(prefix, taget_id), "{}_out_{}_{}".format(prefix, elm[0],elm[1]), label="{0} {1}".format(elm[0], elm[1]))

        for elm in self._edge_list:
            g.edge("{}_{}".format(prefix, elm[0][0]), "{}_{}".format(prefix, elm[1][0]), label=elm[0][1], arrowtail=None)


    def set_plugs(self, target_id, mod_dict):
        for k in mod_dict.keys():
            for i in range(len(self._in_list)):
                plug = self._in_list[i]
                if plug == (target_id, k):
                    self._in_list[i] = (target_id, mod_dict[k])
            for i in range(len(self._out_list)):
                plug = self._out_list[i]
                if plug == (target_id, k):
                    self._out_list[i] = (target_id, mod_dict[k])

    @property
    def node_list(self):
        return self._node_list
    @property
    def in_list(self):
        return self._in_list
    @property
    def out_list(self):
        return self._out_list
    @property
    def edge_list(self):
        return self._edge_list


class LogicCanvas:
    def __init__(self):
        self.count = 0
        self.block_dict = {}
        self.history_dict = {}

    def Ent(self, kind, in_list=[], out_list=[]):
        id_name = "#{}".format(self.count)
        self.count += 1

        block = LogicBlock(id_name)
        block.Ent_Node(id_name, kind, in_list, out_list)

        self.block_dict[id_name] = block
        self.history_dict[id_name] = ("Ent",[])
        return id_name

    def get_block(self, block_id):
        return self.block_dict[block_id]

    def Prod(self, block_id_1, block_id_2):
        ret = 0
        block_1 = self.block_dict[block_id_1].DeepCopy()
        block_2 = self.block_dict[block_id_2].DeepCopy()
        new_id_name = "#{}".format(self.count)
        self.count += 1
        new_block = LogicBlock(
        new_id_name,
        node_list = block_1.node_list + block_2.node_list,
        in_list = block_1.in_list + block_2.in_list,
        out_list = block_1.out_list + block_2.out_list,
        edge_list = block_1.edge_list + block_2.edge_list
        )
        self.block_dict[new_id_name] = new_block
        self.history_dict[new_id_name] = ("Prod",[block_id_1, block_id_2])
        return ret, new_id_name

    def Comp(self, block_id_1, block_id_2):
        ret = 0
        block_1 = self.block_dict[block_id_1].DeepCopy()
        block_2 = self.block_dict[block_id_2].DeepCopy()

        if len(block_1.out_list) != len(block_2.in_list):
            ret = -1
            return ret, new_block

        num_of_plugs = len(block_1.out_list)
        for i in range(num_of_plugs):
            id_1, node_1 = block_1.out_list[i]
            id_2, node_2 = block_2.in_list[i]
            if node_2 != 'X' and node_2 != 'Y' and not (node_1 == node_2):
                print(node_1)
                print(node_2)
                ret = -2
                return ret, LogicBlock('')

        for i in range(num_of_plugs):
            # print(i)
            id_1, node_1 = block_1.out_list[i]
            id_2, node_2 = block_2.in_list[i]
            # print(node_2)
            if node_2 == 'X' or node_2 == 'Y':
                block_2.set_plugs(id_2, {node_2:node_1})

        new_edge_list = block_1.edge_list + block_2.edge_list
        for i in range(num_of_plugs):
            node_1 = block_1.out_list[i]
            node_2 = block_2.in_list[i]
            new_edge_list.append((node_1, node_2))

        new_id_name = "#{}".format(self.count)
        self.count += 1
        new_block = LogicBlock(
        new_id_name,
        node_list = block_1.node_list + block_2.node_list,
        in_list = block_1.in_list,
        out_list = block_2.out_list,
        edge_list = new_edge_list
        )
        self.block_dict[new_id_name] = new_block
        self.history_dict[new_id_name] = ("Comp",[block_id_1, block_id_2])
        return ret, new_id_name

    def Lamb(self, block_id, in_plug_1, in_plug_2):
        ret = 0
        target_block = self.block_dict[block_id].DeepCopy()

        out_plug = "{}=>{}".format(in_plug_1[1], in_plug_2[1])
        node_id_name = "#{}".format(self.count)
        self.count += 1
        block = LogicBlock(node_id_name)
        block.Ent_Node(node_id_name, "junction", [in_plug_1[1], in_plug_2[1]], [out_plug])

        new_node_list = target_block.node_list + block.node_list
        new_in_list = target_block.in_list
        new_out_list = target_block.out_list + block.out_list
        new_in_list.remove(in_plug_1)
        new_out_list.remove(in_plug_2)
        new_edge_list = target_block.edge_list + block.edge_list
        new_edge_list.append((in_plug_1, (node_id_name, in_plug_1[1])))
        new_edge_list.append((in_plug_2, (node_id_name, in_plug_2[1])))

        new_id_name = "#{}".format(self.count)
        self.count += 1
        new_block = LogicBlock(
        new_id_name,
        node_list = new_node_list,
        in_list = new_in_list,
        out_list = new_out_list,
        edge_list = new_edge_list
        )
        self.block_dict[new_id_name] = new_block
        self.history_dict[new_id_name] = ("Lamb",[block_id])
        return ret, new_id_name

    def Up(self, block_id, in_plug):
        ret = 0
        target_block = self.block_dict[block_id].DeepCopy()

        insert_flag = False
        same_flag = False
        new_in_list = []
        for plug in target_block.in_list:
            new_in_list.append(plug)
            if (not same_flag) and (plug[0] == in_plug[0]):
                same_flag = True
            if (same_flag) and (plug[0] != in_plug[0]):
                new_in_list.append(in_plug)
                insert_flag = True

        if not insert_flag:
            new_in_list.append(in_plug)

        new_id_name = "#{}".format(self.count)
        self.count += 1
        new_block = LogicBlock(
        new_id_name,
        node_list = target_block.node_list,
        in_list = new_in_list,
        out_list = target_block.out_list,
        edge_list = target_block.edge_list
        )
        self.block_dict[new_id_name] = new_block
        self.history_dict[new_id_name] = ("Up",[block_id])
        return ret, new_id_name

    def create_graph(self, block_id, fname, format='png'):
        ret_list = []
        self.search_history_dict(block_id, ret_list)
        # print("ret_list={}".format(ret_list))
        g = Digraph('G', format=format)
        g.attr(compound='true')
        self.create_history_graph(ret_list, g)
        g.render(fname)

    def search_history_blocks(self, block_id, ret_block_id_list):
        cmd, blk_ids_list = self.history_dict[block_id]
        for blk_id in blk_ids_list:
            self.search_history_blocks(blk_id, ret_block_id_list)
        for blk_id in blk_ids_list:
            ret_block_id_list.append(blk_id)

    def search_history_dict(self, block_id, ret_history_list):
        cmd, blk_ids_list = self.history_dict[block_id]
        for blk_id in blk_ids_list:
            self.search_history_dict(blk_id, ret_history_list)
        ret_history_list.append((cmd, blk_ids_list, block_id))

    def create_history_graph(self, history_list, g):
        for h in reversed(history_list):
            cmd, blk_ids_list, rslt_blk = h
            blk = self.block_dict[rslt_blk]
            with g.subgraph(name="cluster_{}".format(rslt_blk)) as c:
                c.attr(style='filled')
                c.attr(color='lightgrey')
                c.node_attr.update(style='filled', color='white')
                blk.create_block_graph(c, prefix=rslt_blk)
                c.attr(label="cluster_{}".format(rslt_blk))
            cmd, blk_ids_list, rslt_blk = h
            cmd_node_name = "{}_{}".format(rslt_blk,cmd)
            g.node(cmd_node_name, style='filled', color='skyblue')


            cmd_node_name = "{}_{}".format(rslt_blk,cmd)
            blk = self.block_dict[rslt_blk]
            # in_node = blk.in_list[0]
            in_node = blk.in_list[-1]
            node_name = "{}_in_{}_{}".format(rslt_blk,in_node[0],in_node[1])
            g.edge(cmd_node_name, node_name, lhead="cluster_{}".format(rslt_blk))

        for h in history_list:
            cmd, blk_ids_list, rslt_blk = h
            cmd_node_name = "{}_{}".format(rslt_blk,cmd)
            for blk_id in blk_ids_list:
                blk = self.block_dict[blk_id]
                # out_node = blk.out_list[0]
                out_node = blk.out_list[-1]
                node_name = "{}_out_{}_{}".format(blk_id,out_node[0],out_node[1])
                g.edge(node_name, cmd_node_name, ltail="cluster_{}".format(blk_id))
