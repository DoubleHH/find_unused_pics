#! /usr/bin/python
# -*- coding:utf-8 -*-

import shutil
import os
import time
import glob
from sys import argv

#from colorama import init, Fore, Back, Style
#init(autoreset=True)    #  初始化，并且设置颜色设置自动恢复
#print(Fore.RED + 'some red text')

def find_all_pngs(image_path):
    command = 'ag -l -g "\.png$" %s' % (image_path)
    pics = os.popen(command).readlines()
    all_pic = {}
    for pic in pics:
        picnames = pic.split('/')
        if len(picnames) <= 0:
            continue
        pic_name = picnames[-1]
        pic_name = pic_name[:-5]
        pic_name = pic_name.replace('@2x', '').replace('@3x', '')
        # print pic
        # print pic_name
        if pic_name not in all_pic.keys():
            all_pic[pic_name] = pic
    print "all pics :"
    print '\n'.join(all_pic.keys())
    print "all count(include 2x 3x) : %s, unique name pics : %s" % (len(pics), len(all_pic))
    return all_pic

def find_unused_pics(image_path, search_path):

    pics = find_all_pngs(image_path)

    print "Start searching unused images"
    #找出未使用的图片
    unused_pics = {}
    index = 0
    length = len(pics.keys())
    for pic in set(pics.keys()):
        index = index + 1
        print "当前搜索进度：%s" % (index * 100.0 / length)
        # if index > 20:
        #     break
        command = r'ag -l "@\"%s" %s' % (pic, search_path)
        # command = r'ag -g "\"%s" %s' % (pic, search_path)
        # print command
        result = os.popen(command).readlines()

        # print result
        # print "len:", len(result)
        if len(result) == 0:
            unused_pics[pic] = pics[pic]

    #将未使用的图片文件名保存到文本
    # txt_path = 'unused_pic.txt'
    # txt = '\n'.join(sorted(unused_pics))
    # os.system('echo "%s" > %s'%(txt, txt_path))

    print '\033[0;31;40m'
    print '*' * 20 ,  "未使用的图片", '*' * 20
    for pic in set(unused_pics.keys()):
    	print '\t', pic
    print '*' * 50
    print "total unused pic count : %s" % len(unused_pics)
    print 'Done!'
    print '\033[0m'
    return unused_pics

def mk_new_dir(path):
    path = path.strip()
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def delete_unused_image(unused_pics):
    path = os.path.abspath('.') + "/unused_pics"
    mk_new_dir(path)
    # save unused pic
    if os.path.exists(path):
        for pic_path in unused_pics.values():
            pic_path_dealed = pic_path.strip().strip('\n')
            shutil.copy(pic_path_dealed,  path)
            os.remove(pic_path_dealed)


if __name__ == '__main__':

    if len(argv) < 3:
        print "参数错误：\n第一个参数图片的文件夹，\n第二个参数是要搜索的文件夹"
        print "Usage: python find_unused_pics.py images_path search_path del(option)"
        exit(0)
    print "image folder: %s" % (argv[1])
    print "code folder: %s" % (argv[2])
    # find_all_pngs(argv[1])
    st_time = time.time()
    unused_pics = find_unused_pics(argv[1], argv[2])
    ed_time = time.time()
    print "total find time: %s" % (ed_time - st_time)
    if len(argv) > 3 and argv[3] == 'del':
        delete_unused_image(unused_pics)
