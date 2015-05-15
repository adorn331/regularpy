#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'aducode@126.com'

operators = ['|', '*', '(', ')']  # 支持的操作符
operator_priority = {'|': 1, '.': 2, '*': 3, } # 运算符优先级
operations_num = {'|': 2, '.': 2, '*': 1, }  # 运算符的操作数


class Node(object):
    """
    AST节点
    """
    def __init__(self, value, childrens=None):
        self.value = value
        self.childrens = childrens

    def add_children(self, children):
        if self.childrens is None:
            self.childrens = []
        self.childrens.append(children)

    def __str__(self):
        return '%s:%s' % (self.value, self.childrens)


def build(token):
    """
    根据输入的正则表达式构建抽象语法树
    :param token:  正则表达式
    :return:       AST root
    """
    value_stack = []  # 字符栈
    operator_stack = [] # 操作符栈
    is_operator = False
    for t in token:
        if t in operators:
            # 操作符
            op = t
            if op != '*':
                is_operator = True
            else:
                is_operator = False
            while operator_stack and operator_priority[operator_stack[-1]] >= operator_priority[op]:
                # 操作符栈栈顶优先级高于当前操作符
                # 需要先计算
                _op = operator_stack.pop()
                node = Node(_op)
                for i in xrange(operations_num[_op]):
                    node.add_children(value_stack.pop())
                value_stack.append(node)
            operator_stack.append(op)
        else:
            # 字符
            if not is_operator and token[0] != t:
                # 说明前一个t也是一个字符串，两个字符串之间是cat操作(用 . 代替)
                op = '.'
                while operator_stack and operator_stack and operator_priority[operator_stack[-1]] >= operator_priority[op]:
                    _op = operator_stack.pop()
                    node = Node(_op)
                    for i in xrange(operations_num[_op]):
                        node.add_children(value_stack.pop())
                    value_stack.append(node)
                operator_stack.append(op)
                is_operator = True
            # 说明前一个是一个操作符
            value = t
            is_operator = False
            value_stack.append(Node(value))  # 压站
    while operator_stack:
        op = operator_stack.pop()
        node = Node(op)
        for i in xrange(operations_num[op]):
            node.add_children(value_stack.pop())
        value_stack.append(node)
    return value_stack[0]



if __name__ == '__main__':
    re = raw_input("please input regular text:\n")
    while re!='quit':
        root = build(re)
        re = raw_input("please input regular text:\n")


