# -*- coding: utf-8 -*-
import os
from logic import LogicCanvas

def main():
    canvas = LogicCanvas()
    id_01_f     = canvas.Ent("f",    in_list=['A', 'B'], out_list=['C'])
    id_02_dup   = canvas.Ent("dup",  in_list=['X'],      out_list=['X', 'X'])
    id_03_g     = canvas.Ent("g",    in_list=['C', 'C'], out_list=['D'])

    id_04_id    = canvas.Ent("id",   in_list=['A'],      out_list=['A'])
    id_05_h     = canvas.Ent("h",    in_list=['A'],      out_list=['C', 'D'])
    id_06_swap  = canvas.Ent("swap", in_list=['X', 'Y'], out_list=['Y', 'X'])

    id_07_codup = canvas.Ent("codup",in_list=['X', 'X'], out_list=['X'])
    id_08_id    = canvas.Ent("id",   in_list=['X'],      out_list=['X'])

    id_09_swap  = canvas.Ent("swap", in_list=['C', 'D'], out_list=['D', 'C'])
    id_10_i     = canvas.Ent("i",    in_list=['D', 'C'], out_list=['A'])
    id_11_id    = canvas.Ent("id",   in_list=['X'],      out_list=['X'])

    # Left
    ret, id_12_comp = canvas.Comp(id_01_f, id_02_dup)
    ret, id_13_comp = canvas.Comp(id_12_comp, id_03_g)

    ret, id_14_comp = canvas.Comp(id_04_id, id_05_h)
    ret, id_15_comp = canvas.Comp(id_14_comp, id_06_swap)

    ret, id_16_prod = canvas.Prod(id_13_comp, id_15_comp)
    ret, id_17_prod = canvas.Prod(id_07_codup, id_08_id)

    ret, id_18_comp = canvas.Comp(id_16_prod, id_17_prod)

    # Right
    ret, id_19_comp = canvas.Comp(id_09_swap, id_10_i)
    ret, id_20_lamb = canvas.Lamb(id_19_comp, ("#8", 'C'), ("#9", 'A'))
    ret, id_21_comp = canvas.Comp(id_20_lamb, id_11_id)

    # Merge
    ret, id_22_prod = canvas.Prod(id_18_comp, id_21_comp)

    # Create graph
    print("dump")
    outputs_dir = "results"
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    graph_path = os.path.join(outputs_dir, "graph_A22P11.dot")

    canvas.get_block(id_22_prod).dump()
    # canvas.get_block(id_22_prod).create_graph(graph_path, format='png')
    # canvas.get_block(id_22_prod).create_graph(graph_path, format='svg')
    canvas.create_graph(id_22_prod, graph_path, format="png")
    canvas.create_graph(id_22_prod, graph_path, format="svg")

if __name__ == '__main__':
    main()
