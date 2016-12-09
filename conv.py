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
            key = key.decode('utf-8') # 转换为unicode
            val = lines2[i].strip()
            self.update({key:val})
        f1.close()
        f2.close()
                

def convertPoints2BndBox(points):
    xmin = sys.maxint
    ymin = sys.maxint
    xmax = -sys.maxint
    ymax = -sys.maxint
    for p in points:
        x = p[0]
        y = p[1]
        xmin = min(x,xmin)
        ymin = min(y,ymin)
        xmax = max(x,xmax)
        ymax = max(y,ymax)

    # Martin Kersner, 2015/11/12
    # 0-valued coordinates of BB caused an error while
    # training faster-rcnn object detector.
    if (xmin < 1):
        xmin = 1

    if (ymin < 1):
        ymin = 1

    return (int(xmin), int(ymin), int(xmax), int(ymax))

def conv_one(fname, **kwargs):
    # 转换一个 xml 文件
    remap = kwargs['remap']
    folder = kwargs['folder']
    reader = PascalVocReader(fname)
    shapes = reader.shapes
    for s in shapes:
        if s[0] in remap.keys():
            s[0] = remap[s[0]]

    basename = os.path.basename(fname)
    mainname,_ = os.path.splitext(basename)
    writer = PascalVocWriter(folder, mainname + '.jpg', reader.imgsize)
    for s in shapes:
        b = convertPoints2BndBox(s[1])
        writer.addBndBox(b[0],b[1],b[2],b[3], s[0], s[4], s[5], s[6]) 
    writer.save(targetFile=mainname + '.xml')



def conv_dir(dname, **kwargs):
    # 转换一个目录下的所有 xml 文件
    kwargs.update({'folder':'VOC2007'})
    for fname in os.listdir(dname):
        _, ext = os.path.splitext(fname)
        if ext == '.xml':
            fname = os.path.sep.join([dname, fname])
            conv_one(fname, **kwargs)


if __name__ == '__main__':
    conv_dir(sys.argv[1], 
            remap=remap('data/predefined_classes.txt', 'data/predefined_classes.txt.en'))



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

