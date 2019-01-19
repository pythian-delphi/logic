# -*- coding: utf-8 -*-
import os
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
            g.node("{}_in_{}_{}".format(prefix, elm[0],elm[1]), label=elm[1])

        g.attr('node', shape='ellipse')
        for elm in self._node_list:
            # g.node("{}_{}".format(elm[0],elm[1]))
            g.node("{}_{}".format(prefix, elm[0]), label=elm[1])

        g.attr('node', shape='box')
        for elm in self._out_list:
            g.node("{}_out_{}_{}".format(prefix, elm[0],elm[1]), label=elm[1])

        # Edge
        for elm in self._in_list:
            taget_id = elm[0]
            g.edge("{}_in_{}_{}".format(prefix, elm[0],elm[1]), "{}_{}".format(prefix, taget_id), label=elm[1])

        for elm in self._out_list:
            taget_id = elm[0]
            g.edge("{}_{}".format(prefix, taget_id), "{}_out_{}_{}".format(prefix, elm[0],elm[1]), label=elm[1])

        for elm in self._edge_list:
            g.edge("{}_{}".format(prefix, elm[0][0]), "{}_{}".format(prefix, elm[1][0]), label=elm[0][1])


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

    def Ent(self, kind):
        id_name = "#{}".format(self.count)
        self.count += 1
        block = LogicBlock(id_name)
        if kind == "id":
            block.Ent_Node(id_name, "id", ['X'], ['X'])
        elif kind == "dup":
            block.Ent_Node(id_name, "dup", ['X'], ['X', 'X'])
        elif kind == "swap":
            block.Ent_Node(id_name, "swap", ['X', 'Y'], ['Y', 'X'])
        elif kind == "a":
            block.Ent_Node(id_name, "a", ['A', 'B'], ['A'])
        elif kind == "b":
            block.Ent_Node(id_name, "b", ['B'], ['B', 'A'])
        elif kind == "c":
            block.Ent_Node(id_name, "c", ['A', 'B'], ['C'])
        elif kind == "d":
            block.Ent_Node(id_name, "d", ['C'], ['A'])
        else:
            block.Ent_Node(id_name)

        self.block_dict[id_name] = block
        self.history_dict[id_name] = ("Ent",[])
        return id_name

    def get_block(self, block_id):
        return self.block_dict[block_id]

    def Prob(self, block_id_1, block_id_2):
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
        self.history_dict[new_id_name] = ("Prob",[block_id_1, block_id_2])
        return ret, new_id_name

    def Comp(self, block_id_1, block_id_2):
        ret = 0
        block_1 = self.block_dict[block_id_1].DeepCopy()
        block_2 = self.block_dict[block_id_2].DeepCopy()

        # print("hoge 1")
        if len(block_1.out_list) != len(block_2.in_list):
            ret = -1
            return ret, new_block

        # print("hoge 2")
        num_of_plugs = len(block_1.out_list)
        for i in range(num_of_plugs):
            id_1, node_1 = block_1.out_list[i]
            id_2, node_2 = block_2.in_list[i]
            if node_2 != 'X' and node_2 != 'Y' and not (node_1 == node_2):
                print(node_1)
                print(node_2)
                ret = -2
                return ret, LogicBlock('')

        # print("hoge 3")
        # print("num_of_plugs = {}".format(num_of_plugs))
        for i in range(num_of_plugs):
            print(i)
            id_1, node_1 = block_1.out_list[i]
            id_2, node_2 = block_2.in_list[i]
            print(node_2)
            if node_2 == 'X' or node_2 == 'Y':
                # print({node_2:node_1})
                # print(block_2.in_list)
                # print(block_2.out_list)
                block_2.set_plugs(id_2, {node_2:node_1})
                # print(block_2.in_list)
                # print(block_2.out_list)


        # print("hoge 4")
        new_edge_list = block_1.edge_list + block_2.edge_list
        for i in range(num_of_plugs):
            node_1 = block_1.out_list[i]
            node_2 = block_2.in_list[i]
            new_edge_list.append((node_1, node_2))

        # print("hoge 5")
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

    def create_graph(self, block_id, fname, format='png'):
        ret_list = []
        self.search_history_dict(block_id, ret_list)
        print(ret_list)
        # exit(1)
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


def main():
    canvas = LogicCanvas()
    id_1_b = canvas.Ent("b")
    id_2_b = canvas.Ent("b")

    id_3_id = canvas.Ent("id")
    id_4_a = canvas.Ent("a")
    id_5_id = canvas.Ent("id")

    id_6_swap = canvas.Ent("swap")
    id_7_id = canvas.Ent("id")

    id_8_a = canvas.Ent("a")
    id_9_id = canvas.Ent("id")

    ret, id_10_prob = canvas.Prob(id_1_b, id_2_b)

    ret, id_11_prob = canvas.Prob(id_3_id, id_4_a)
    ret, id_12_prob = canvas.Prob(id_11_prob, id_5_id)

    ret, id_13_prob = canvas.Prob(id_6_swap, id_7_id)

    ret, id_14_prob = canvas.Prob(id_8_a, id_9_id)

    ret, id_15_comp = canvas.Comp(id_10_prob, id_12_prob)
    ret, id_16_comp = canvas.Comp(id_15_comp, id_13_prob)
    ret, id_17_comp = canvas.Comp(id_16_comp, id_14_prob)

    print("dump")
    canvas.get_block(id_17_comp).dump()

    # Create graph
    outputs_dir = "results"
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    graph_path = os.path.join(outputs_dir, "graph_8.dot")
    canvas.create_graph(id_17_comp, graph_path, format="png")
    canvas.create_graph(id_17_comp, graph_path, format="svg")

if __name__ == '__main__':
    main()
