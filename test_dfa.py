#!/usr/bin/python
# -*-  coding:utf-8 -*-
__author__ = 'aducode@126.com'
from dfa.tree import build_ast
from dfa.dfa import build_dfa


def match(dfa, text):
    start_state = dfa[0]
    end_states = dfa[1]
    trans = dfa[3]
    current_state = start_state
    for t in text:
        current_state = trans[current_state].get(t, None)
        if not current_state:
            current_state = start_state
        elif current_state in end_states:
            return True
    return False

def group(dfa, text):
    """
    最小匹配
    :param dfa:
    :param text:
    :return:
    """
    start_state = dfa[0]
    end_states = dfa[1]
    trans = dfa[3]
    current_state = start_state
    start = end = 0
    for i in xrange(len(text)):
        t = text[i]
        current_state = trans[current_state].get(t, None)
        if not current_state:
            current_state = start_state
            start = i+1
        elif current_state in end_states:
            end = i+1
            yield text[start:end]
            current_state = start_state
            start = i+1

def group2(dfa, text):
    """
    最大匹配
    :param dfa:
    :param text:
    :return:
    """
    start_state = dfa[0]
    end_states = dfa[1]
    trans = dfa[3]
    current_state = start_state
    start = 0
    end = -1
    i = 0
    while i < len(text):
        t = text[i]
        current_state = trans.get(current_state, {}).get(t, None)
        if not current_state:
            if end != -1:
                yield text[start:end]
                start = i = end
            else:
                i = start + 1
                start = i
            current_state = start_state
            end = -1
        else:
            if current_state in end_states:
                end = i+1
            i += 1
    if end != -1:
        yield text[start:end]


if __name__ == '__main__':
    re = raw_input("please input regular text:(input /quit to quit)\n")
    while re != '/quit':
        if re.startswith('/'):
            re = raw_input("can't contain '/', input another regular text:\n")
            continue
        tree = build_ast(re)
        # visit_ast(root)
        dfa = build_dfa(tree)
        # print 'start state:', dfa[0]
        # print 'end states:', dfa[1]
        # print 'states:', dfa[2]
        # print 'trans:', dfa[3]
        text = raw_input('please input text:(input /pattern for a new pattern)\n')
        while text != '/pattern':
            print '-' * 20
            # print 'is match?\t', 'yes' if match(dfa, text) else 'no'
            for t in group2(dfa, text):
                print t
            text = raw_input('please input text:(input /pattern for a new pattern)\n')
        re = raw_input("please input regular text:(input /quit to quit)\n")
    print 'Bye~~'
