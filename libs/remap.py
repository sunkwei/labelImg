#!/usr/bin/python
# coding: utf-8
#
# @file: remap.py
# @date: 2016-12-09
# @brief:
# @detail:
#
#################################################################

class LineList(list):
    # 从文件中加载，每行一个，忽略 空行，# 开始行
    def __init__(self, fname):
        with open(fname) as f:
            for line in f:
                line = line.strip()
                if not line or line[0] == '#':
                    continue
                self.append(line)


class remap(dict):
    # 建立映射，从l1, 到l2
    def __init__(self, fn1, fn2):
        l1 = LineList(fn1)
        l2 = LineList(fn2)
        self.update(zip(l1, l2))


    def conv(self, f):
        if f in self.keys():
            return self[f]
        else:
            return f



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

