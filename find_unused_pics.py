#! /usr/bin/python
# -*- coding:utf-8 -*-

import shutil
import os
import time
import glob
import re
from sys import argv
import find_unused_pics_public
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser(usage="python %prog [optinos] image_path search_path")
    parser.add_option("-a", "--android",
                    action = "store_true",
                    dest = "android",
                    default = False,
                    help = u"Search in Android project.(表明是搜索安卓工程)"
                    )
    parser.add_option("-d", "--delete",
                    action = "store_true",
                    dest = "delete",
                    default = False,
                    help = u"Delete the unused pics.(表明搜索到即删除掉，慎用~)"
                    )
    (options, args) = parser.parse_args()
    print options
    print args
    if len(args) <= 0:
        print "参数错误：\n第一个参数图片的文件夹，\n第二个参数是要搜索的文件夹\n[options]指定其他功能用--help或-h来查看"
        print "Usage:python %s [optinos] image_path search_path" % (__file__)
        exit(0)
    st_time = time.time()
    search_path = None
    if len(args) > 1:
        search_path = args[1]
    unused_pics = find_unused_pics_public.find_unused_pics(args[0], search_path, not options.android)
    ed_time = time.time()
    total_time = "Searching total time: %.1f seconds" % (ed_time - st_time)
    find_unused_pics_public.print_color_string(total_time, "lred")
    if options.delete:
        find_unused_pics_public.delete_unused_image(unused_pics)
