#! /usr/bin/python
# -*- coding:utf-8 -*-

import shutil
import os
import time
import glob
import re
from sys import argv
from os.path import join, getsize

COLORS  = {
    "blue": "0;34m",
    "green": "0;32m",
    "cyan": "0;36m",
    "red": "0;31m",
    "purple": "0;35m",
    "brown": "0;33m",
    "yellow": "1;33m",
    "lred": "1;31m",
    "o_yellow": "3;1;33m",
}

def print_color_string(string, color="red"):
    if not string or len(string) == 0:
        return
    print ("\033[" + COLORS[color] + string + "\033[0m")

def print_progress(progress, total):
    maxCount = 40
    ratio = progress * 1.0 / total 
    progress_count = int(round(ratio * maxCount))
    result = "progress: " + "✓" * progress_count + "✘" * (maxCount - progress_count) + ("    %05.2f%%" % (ratio * 100))
    print_color_string(result, "o_yellow")

def find_all_pngs(image_path, is_ios):
    command = 'ag -l -g "\.png$" %s' % (image_path)
    pics = os.popen(command).readlines()
    all_pic = {}
    for pic in pics:
        pic = pic.strip().strip("\n")
        picnames = pic.split('/')
        if len(picnames) <= 0:
            continue
        if is_ios:
            # iOS
            pic_pre_path = picnames[-2]
            # Appicon and launch image
            if pic_pre_path.endswith(".appiconset") or pic_pre_path.endswith(".launchimage"):
                continue
            imageset_suffix = ".imageset"
            if pic_pre_path.endswith(imageset_suffix):
                pic_name = pic_pre_path[:-len(imageset_suffix)]
                png_real_name = picnames[-1].replace(".png", "").replace("@2x", "").replace("@3x", "")
                if cmp(png_real_name, pic_name) != 0:
                    print_color_string("imageset图片与png名称不一致: %s" % pic)
            else:
                pic_name = picnames[-1]
                pic_name = pic_name[:-4]
                index = pic_name.find("@2x")
                if index == -1:
                    index = pic_name.find("@3x")
                if index != -1:
                    pic_name = pic_name[:index]
                    if len(pic_name) <= 0:
                        print_color_string("图片命名有问题: %s" % pic)
                        continue
            if picnames[-1].find("@2x") == -1 and picnames[-1].find("@3x") == -1:
                print_color_string("单倍图: %s" % pic)
        else:
            # Android
            pic_name = picnames[-1]
            pic_name = pic_name[:-4]
        array = all_pic.get(pic_name)
        if array == None:
            array = []
            all_pic[pic_name] = array
        array.append(pic)
    # print_color_string("all pics :", "lred")
    # print '\n'.join(all_pic.keys())
    if is_ios:
        summary = "all count(include 2x 3x) : %s, unique name pics : %s\nnot include appicon and launchimages" % (len(pics), len(all_pic))
    else:
        summary = "all count : %s" % (len(all_pic))
    print_color_string(summary, "brown")
    return all_pic

def find_unused_pics(image_path, search_path, is_ios):
    pics = find_all_pngs(image_path, is_ios)
    print_color_string("Start searching unused images", "green")
    if search_path == None:
        print_color_string("已搜完所有图片，如果想找到未使用的图片，请指定搜索路径~", "red")
        return
    #找出未使用的图片
    unused_pics = {}
    index = 0
    keys = pics.keys()
    length = len(keys)
    for pic in keys:
        index = index + 1
        print_progress(index, length)
        # if index > 0:
        #     break
        if is_ios:
            pattern = "\\\"%s" % (pic)
        else:
            android_pic = pic
            if android_pic.endswith(".9"):
                android_pic = android_pic[:-2]
            pattern = ("\\\"@drawable/%s\\\"" % android_pic) + "|" + \
                        ("R.drawable.%s" % android_pic) + "|" + \
                        ("\\\"%s\\\"" % android_pic)
        command = r"ag -lac '%s' %s" % (pattern, search_path)
        result = os.popen(command).readlines()
        result_count = len(result)
        if result_count == 0:
            unused_pics[pic] = pics[pic]
        elif is_ios and result_count == 1 and (result[0]).find(image_path) >= 0:
            unused_pics[pic] = pics[pic]
    doubtful_keys = []
    pattern = pattern = re.compile(r'.*\d+')
    unused_size = 0
    for pic in unused_pics.keys():
        result = pattern.match(pic)
        unused_size += sum([getsize(path) for path in unused_pics[pic]])
        if result != None:
            if is_ios or pic.endswith(".9") == False:
                doubtful_keys.append(pic)
    unused_keys = set(unused_pics.keys())
    print '\033[0;31;40m'
    print '*' * 20 ,  ("未使用的图片：%s个" % len(unused_keys)), '*' * 20
    for pic in unused_keys:
    	print '\t', pic
    print '*' * 50
    print "total unused pic count : %s, all size: %d bytes" % (len(unused_pics), unused_size)
    print 'Done!'
    print '\033[0m'
    # print doubtful keys
    print_color_string("注意：可能程序中特殊处理用到的图片，%d个" % (len(doubtful_keys)), "purple")
    print_color_string('\n'.join(doubtful_keys), "brown")

    for value in doubtful_keys:
        del unused_pics[value]

    return unused_pics

def mk_new_dir(path):
    path = path.strip()
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def delete_unused_image(unused_pics, is_ios):
    print_color_string("Start remove %d pictures or imageset" % (len(unused_pics)), "green")
    path = os.path.abspath('.') + "/unused_pics/"
    mk_new_dir(path)
    # save unused pic
    if os.path.exists(path):
        for pic_path_array in unused_pics.values():
            pic_path = pic_path_array[0]
            is_dir = False
            to_path = path
            if is_ios:
                # check is imageset
                pic_path_splits = pic_path.split("/")
                if pic_path_splits[-2].endswith(".imageset"):
                    to_path += pic_path_splits[-2]
                    is_dir = True
                    pic_path_splits.pop()
                    pic_path = "/".join(pic_path_splits)
            if is_dir:
                shutil.copytree(pic_path, to_path)
                shutil.rmtree(pic_path)
            else:
                shutil.copy(pic_path, to_path)
                os.remove(pic_path)
            print "remove %s, cp to: %s" % (pic_path, to_path)
