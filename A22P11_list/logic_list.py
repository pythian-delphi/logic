# -*- coding: utf-8 -*-

class LogicListType:
    type_and = -1
    type_none = 0
    type_or = 1

class LogicList:
    def __init__(self, list_type=LogicListType.type_none, contents=[]):
        self._list_type = list_type
        self._list_contents = contents
    def __str__(self):
        return "({0}, {1})".format(self._list_type, self._list_contents)
    def __repr__(self):
        return "({0}, {1})".format(self._list_type, self._list_contents)
    @property
    def list_type(self):
        return self._list_type
    @property
    def list_contents(self):
        return self._list_contents
    @property
    def logic_list(self):
        return (self._list_type, self._list_contents)

    def DeepCopy(self):
        new_list = LogicList(list_type=self.list_type, contents=list(self._list_contents))
        return new_list

    def dump(self):
        print(self.logic_list)

    @classmethod
    def __Sequen_List(cls, logic_list, ret_string):
        delimiter = '|' if logic_list[0] == LogicListType.type_or else ','
        for elm in logic_list[1]:
            if type(elm) is tuple:
                ret_string.extend("(".format(delimiter))
                LogicList.__Sequen_List(elm, ret_string)
                ret_string.extend("){}".format(delimiter))
            else:
                ret_string.extend("{0}{1}".format(elm, delimiter))
        if (ret_string[-1] == '|') or (ret_string[-1] == ','):
            ret_string.pop()

    def Sequen_List(self):
        ret_str_list = []
        LogicList.__Sequen_List(self.logic_list, ret_str_list)
        return "".join(ret_str_list)

    def __add__(self, other):
        ret_list = LogicList(list_type=LogicListType.type_or, contents=[self.logic_list, other.logic_list])
        if (self.list_type != LogicListType.type_and) and (other.list_type != LogicListType.type_and):
            ret_list = LogicList(list_type=LogicListType.type_or, contents=(self.list_contents + other.list_contents))
        return ret_list

    def __mul__(self, other):
        ret_list = LogicList(list_type=LogicListType.type_and, contents=[self.logic_list, other.logic_list])
        if (self.list_type != LogicListType.type_or) and (other.list_type != LogicListType.type_or):
            ret_list = LogicList(list_type=LogicListType.type_and, contents=(self.list_contents + other.list_contents))
        return ret_list
