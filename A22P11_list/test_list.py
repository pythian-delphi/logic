# -*- coding: utf-8 -*-
from logic_list import LogicListType, LogicList

def main():
    list_none_1 = LogicList(list_type=LogicListType.type_none, contents=['X'])
    list_none_2 = LogicList(list_type=LogicListType.type_none, contents=['Y'])

    list_and_1 = LogicList(list_type=LogicListType.type_and, contents=['A', 'B'])
    list_and_2 = LogicList(list_type=LogicListType.type_and, contents=['C', 'D'])

    list_or_1 = LogicList(list_type=LogicListType.type_or, contents=['G', 'H'])
    list_or_2 = LogicList(list_type=LogicListType.type_or, contents=['I', 'J'])

    list_sum_none = list_none_1 + list_none_2
    list_sum_and = list_and_1 + list_and_2
    list_sum_or = list_or_1 + list_or_2
    list_sum_none.dump()
    list_sum_and.dump()
    list_sum_or.dump()
    print(list_sum_none.Sequen_List())
    print(list_sum_and.Sequen_List())
    print(list_sum_or.Sequen_List())

    list_sum_and_1 = list_none_1 + list_and_1
    list_sum_and_2 = list_and_1 + list_none_1
    list_sum_and_1.dump()
    list_sum_and_2.dump()
    list_sum_or_1 = list_none_1 + list_or_1
    list_sum_or_2 = list_or_1 + list_none_1
    list_sum_or_1.dump()
    list_sum_or_2.dump()
    list_sum_or_and = list_or_1 + list_and_1
    list_sum_and_or = list_and_1 + list_or_1
    list_sum_or_and.dump()
    list_sum_and_or.dump()
    print(list_sum_and_or.Sequen_List())


    list_prod_none = list_none_1 * list_none_2
    list_prod_and = list_and_1 * list_and_2
    list_prod_or = list_or_1 * list_or_2
    list_prod_none.dump()
    list_prod_and.dump()
    list_prod_or.dump()
    print(list_prod_none.Sequen_List())
    print(list_prod_and.Sequen_List())
    print(list_prod_or.Sequen_List())

    list_prod_and_1 = list_none_1 * list_and_1
    list_prod_and_2 = list_and_1 * list_none_1
    list_prod_and_1.dump()
    list_prod_and_2.dump()
    list_prod_or_1 = list_none_1 * list_or_1
    list_prod_or_2 = list_or_1 * list_none_1
    list_prod_or_1.dump()
    list_prod_or_2.dump()
    list_prod_or_and = list_or_2 * list_and_2
    list_prod_and_or = list_and_2 * list_or_2
    list_prod_or_and.dump()
    list_prod_and_or.dump()
    print(list_prod_and_or.Sequen_List())

    # Sequent
    print("")
    print("Sequent example:")
    print("{0} -> {1}".format(list_prod_and.Sequen_List(), list_sum_or.Sequen_List()))


if __name__ == '__main__':
    main()
