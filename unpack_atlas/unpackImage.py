#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

import sys
import os
import shutil
from PIL import Image


inputResDir = "./unpackRes/"
outResDir = "./desout/"

if not os.path.exists(outResDir):
    os.mkdir(outResDir)

def get_img_item_list(filename):
    """
    获得图片列表
    :param filename:
    :return:
    """
    f = open(filename, 'r', encoding='UTF-8')
    lines = f.readlines()
    print(len(lines))

    image_name = ""
    item_list = []
    i = 0
    group_index = 1
    while True:
        line = lines[i]
        if line == "\n":
            image_name = lines[i+1]
            i += 6
            print("图片名称: " + image_name)
            continue
        item = {}
        group_index = i
        item['image'] = image_name
        item['name'] = lines[group_index].strip()
        item['rotate'] = lines[group_index + 1].split(':')[1].strip()
        item['xy'] = lines[group_index + 2].split(':')[1].strip()
        item['size'] = lines[group_index + 3].split(':')[1].strip()
        item['orig'] = lines[group_index + 4].split(':')[1].strip()
        item['offset'] = lines[group_index + 5].split(':')[1].strip()
        item['index'] = lines[group_index + 6].split(':')[1].strip()

        item_list.append(item)

        i += 7

        if i >= len(lines):
            break
    return item_list


def gen_new_img(item_list, workDir, out_dir):
    """
    生成新图片
    :param item_list:
    :param img_file:
    :param out_dir:
    :return:
    """
    for item in item_list:
        img_file = workDir + "/" + item['image'].replace("\n", "")
        big_image = Image.open(img_file)
        name = item['name']
        is_rotate = item['rotate'] == 'true'
        x = int(item['xy'].split(',')[0].strip())
        y = int(item['xy'].split(',')[1].strip())
        w = int(item['size'].split(',')[0].strip())
        h = int(item['size'].split(',')[1].strip())
        ow = int(item['orig'].split(',')[0].strip())
        oh = int(item['orig'].split(',')[1].strip())

        result_box = (int((ow - w) / 2), int((oh - h) / 2), int((ow + w) / 2), int((oh + h) / 2))
        # 旋转处理
        if is_rotate:
            temp = w
            w = h
            h = temp

        box = [x, y, x + w, y + h]
        rect_on_big = big_image.crop(box)
        # rect_on_big.show()

        if is_rotate:
            rect_on_big = rect_on_big.rotate(-90, expand=True)

        result_image = Image.new('RGBA', (ow, oh), (0, 0, 0, 0))
        result_image.paste(rect_on_big, result_box, mask=0)
        print(item)
        
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        array = name.split('/')
        if len(array) > 1:
            array[-1] = ""
            subdir = out_dir
            for i in range(len(array) - 1):
                subdir = subdir + array[i] + "/"
            if not os.path.exists(subdir):
                os.makedirs(subdir)
        
        outfile = (out_dir + name + '.png')
        result_image.save(outfile)


def unpack(file_dir):
    cwd = file_dir
    path = os.listdir(cwd)
    for p in path:
        d = os.path.splitext(p)
        file_name = d[0]
        file_suffix = d[1]
        if file_suffix == '.atlas':
            # 找png 如果有则切图
            img_file = os.path.join(cwd, file_name + '.png')
            print(img_file)
            if os.path.exists(img_file):
                # 拆图
                # item_list = readFile()
                atlas_file = os.path.join(cwd, p)
                item_list = get_img_item_list(atlas_file)
                out_dir = os.path.join(cwd, '')
                gen_new_img(item_list, cwd, out_dir)
            else:
                print('找不到对应png')















def decrypt_image(inputFile, outFile):
    srcFile = open(inputFile, 'rb')
    outFile = open(outFile, 'wb')

    flag = srcFile.read(3)

    srcdata = bytearray(srcFile.read() )
    # print(flag)
    if flag == b'PKM':
        # print(flag)
        # for x in xrange(0, len(srcdata)):
        #     srcdata[x] = ~(srcdata[x]) & 0xff
        # outFile.write(srcdata)
        return True

    return False


# 把文件夹下所有.png和jpg图片记录下来
def list_all_imgs_in_dir(fromDir, outDir):
    #列出目录下的所有目录
    list = os.listdir(fromDir)
    for line in list:
        # 如果是目录
        tmp_file_path = os.path.join(fromDir, line)
        tmp_out_path = os.path.join(outDir, line)

        if os.path.isdir(tmp_file_path):
	        # 如果目标目录不存在
	        if not os.path.exists(tmp_out_path):
	            os.mkdir(tmp_out_path)

	        list_all_imgs_in_dir(tmp_file_path, tmp_out_path)
        else:
            if tmp_file_path.endswith(".atlas"):
                unpack(fromDir)
                # command = "unpack-spine-atlas.exe -in %s -out %s" % (tmp_file_path, outDir)
                # os.system(command)
                # print(command)
                

list_all_imgs_in_dir(inputResDir, outResDir)
