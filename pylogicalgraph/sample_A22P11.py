# -*- coding: utf-8 -*-

import os
from pylogicalgraph import LogicalGraphCanvas

def main():
    canvas = LogicalGraphCanvas()

    ret,id_01_f     = canvas.Ent("f",    in_list=['A', 'B'], out_list=['C'])
    ret,id_02_dup   = canvas.Ent("dup",  in_list=['X'],      out_list=['X', 'X'])
    ret,id_03_g     = canvas.Ent("g",    in_list=['C', 'C'], out_list=['D'])

    ret,id_04_id    = canvas.Ent("id",   in_list=['A'],      out_list=['A'])
    ret,id_05_h     = canvas.Ent("h",    in_list=['A'],      out_list=['C', 'D'])
    ret,id_06_swap  = canvas.Ent("swap", in_list=['X', 'Y'], out_list=['Y', 'X'])

    ret,id_07_codup = canvas.Ent("codup",in_list=['X', 'X'], out_list=['X'])
    ret,id_08_id    = canvas.Ent("id",   in_list=['X'],      out_list=['X'])

    ret,id_09_swap  = canvas.Ent("swap", in_list=['C', 'D'], out_list=['D', 'C'])
    ret,id_10_i     = canvas.Ent("i",    in_list=['D', 'C'], out_list=['A'])
    ret,id_11_id    = canvas.Ent("id",   in_list=['X'],      out_list=['X'])


    # Create graph
    print("dump")
    outputs_dir = "results"
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    # Left
    ret, id_12_comp = canvas.Comp(id_01_f, id_02_dup)
    ret, id_13_comp = canvas.Comp(id_12_comp, id_03_g)

    ret, id_14_comp = canvas.Comp(id_04_id, id_05_h)
    ret, id_15_comp = canvas.Comp(id_14_comp, id_06_swap)

    ret, id_16_prod = canvas.Prod(id_13_comp, id_15_comp)
    ret, id_17_prod = canvas.Prod(id_07_codup, id_08_id)

    ret, id_18_comp = canvas.Comp(id_16_prod, id_17_prod)

    graph_path = os.path.join(outputs_dir, "left")
    canvas.draw_box(id_18_comp, graph_path)
    canvas.draw_box(id_18_comp, graph_path, format='svg')


    # Right
    ret, id_19_comp = canvas.Comp(id_09_swap, id_10_i)
    ret, id_20_comp = canvas.Comp(id_19_comp, id_11_id)
    ret, id_21_lamb = canvas.Lamb(id_20_comp, "#8_0_0", "#10_0_0")

    graph_path = os.path.join(outputs_dir, "right")
    canvas.draw_box(id_21_lamb, graph_path)
    canvas.draw_box(id_21_lamb, graph_path, format='svg')

    # Merge
    ret, id_22_sum = canvas.Sum(id_18_comp, id_21_lamb)
    canvas.get_logic_box(id_22_sum).dump()

    graph_path = os.path.join(outputs_dir, "A22P11")
    canvas.draw_box(id_22_sum, graph_path)
    canvas.draw_box(id_22_sum, graph_path, format='svg')

if __name__ == '__main__':
    main()
