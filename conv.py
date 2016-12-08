#!/usr/bin/python
# coding: utf-8
#
# @file: conv.py
# @date: 2016-12-08
# @brief:
# @detail:
#
#################################################################

import _init_path
import sys, os
from pascal_voc_io import PascalVocWriter, PascalVocReader

class remap(dict):
    # 建立映射，从l1, 到l2
    def __init__(self, l1, l2):
        f1 = open(l1)
        f2 = open(l2)
        lines1, lines2 = f1.readlines(), f2.readlines()

        if len(lines1) != len(lines2):
            e = '{} {} lines NOT matched!'.format(l1, l2)
            raise Exception(e)

        for i in range(len(lines1)):
            key = lines1[i].strip()
            val = lines2[i].strip()
            self.update({key:val})
        f1.close()
        f2.close()
                


def conv_one(fname, **kwargs):
    # 转换一个 xml 文件
    remap = kwargs['remap']
    reader = PascalVocReader(fname)
    shapes = reader.shapes
    for s in shapes:
        if s.label in remap.keys():
            print 'from {} to {}'.format(s.label, remap[s.label])
            s.label = remap[s.label]

    writer = PascalVocWriter(fname)
    for 




def conv_dir(dname, **kwargs):
    # 转换一个目录下的所有 xml 文件
    for fname in os.listdir(dname):
        _, ext = os.path.splitext(fname)
        if ext == '.xml':
            fname = os.path.sep.join(dname, fname)
            conv_one(fname, kwargs)


if __name__ == '__main__':
    conv_dir(sys.argv[1], remap=remap('data/predefined_classes.txt', 'data/predefined_classes.txt.en'))



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

