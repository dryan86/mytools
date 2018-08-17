#!/usr/bin/env python
# coding=utf-8

import os
import os.path
import argparse
import hashlib
import sqlite3
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import checkSpineVersion as sp

# 资源源路径
################################################
# spine脚本程序路径
spine_app_path = "/Applications/Spine/Spine.app/Contents/MacOS"
# 导出文件格式
export_fileType = ""
# 导入文件路径（角色动作和特效目录）
input_res_path = ""
# 项目导出路径
project_Path = ""
# 默认导出配置
default_config = ""
# 手动配置
manual_config = ""
# 数据库路径
databasePath = ""
# sqlite数据库，后面会初始化
db = False
exportFileList = []
# 失败列表
faildArray = {}
# 忽略列表
ignoreList = {}
# 特殊列表
specialList = {}
allConfigList = {}

TYPE_HERO   = 1
TYPE_UI     = 2
TYPE_EFFECT = 3
################################################
# 通过配置获取参数
def config_getValue(name):
    tmpJson = json.load(file(manual_config))
    return tmpJson[name]

# 检查版本号
def check_version():
    # 检查spine版本
    if sp.checkIsVersion(config_getValue("version")):
        print("Spine版本正确!")
    else:
        print("Spine版本错误! 需要切换到:")
        print(config_getValue("version"))
        os.system(spine_app_path + "/Spine -u " + config_getValue("version"))
        exit()

################################################
# 导出文件
# filePath 需要导出的spine的绝对路径
# outPath 输出到指定位置
def spine_export(config):
    commend = spine_app_path + "/Spine -u " + config_getValue("version") + config
    print commend
    val = os.system(commend)
    return (val == 0)

################################################

#获取一个未使用的配置名
def config_getConfigName():
    i = 0
    while(True):
        newPath = os.path.abspath(__file__ + "/../tmpConfig" + str(i))
        if os.path.exists(newPath):
            i += 1
        else:
            return newPath


# 根据需求生成新的配置文件
def config_createNew(scale):
    if allConfigList.has_key(scale):
        return allConfigList[scale]
    else:
        newFile = config_getConfigName()
        allConfigList[scale] = newFile
        fout = open(newFile, 'w')
        fin = open(default_config, 'r')
        for eachLine in fin:
            index = eachLine.find("\"scale\": ")
            if index != -1:
                fout.write(eachLine[0 : len("\"scale\": ") + index] + "[ " + str(scale) + " ],\n")
            else:
                fout.write(eachLine)
        fin.close()
        fout.close()
        return newFile

# 检查手动配置，是否有指定文件的要求
def config_ignoreORspecial(spineName):
    for ignore in ignoreList:
        if ignore == spineName:
            return True
    for special in specialList:
        if special["name"] == spineName:
            return special["scale"]
    return False

# 删除临时配置文件
def config_removeAllTmpFile():
    i = 0
    while(True):
        newPath = os.path.abspath(__file__ + "/../tmpConfig" + str(i))
        if os.path.exists(newPath):
            os.remove(newPath)
            i += 1
        else:
            break
################################################

# 获取字符串md5
def md5_cal_str(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

# 获取文件的md5
def md5_cal_file(file):
    if os.path.exists(file):
        m = hashlib.md5()
        a_file = open(file, 'rb')
        m.update(a_file.read())
        a_file.close()
        return m.hexdigest()
    else:
        return None

# 获取目录的md5
def md5_cal_folder(dir):
    checkString = ""
    for root, subdirs, files in os.walk(dir):
        files.sort()
        for file in files:
            if file != ".DS_Store":
                filefullpath = os.path.join(root,file)
                filerelpath = os.path.relpath(filefullpath,dir)
                checkString += md5_cal_file(filefullpath)
    return md5_cal_str(checkString)

################################################

# 检查是否需要导出
def db_checkUpdate(path , spinefile ,configScale , storeName):
    # 得到输入目录的md5
    folderMd5 = md5_cal_folder(path)
    # 获取导出文件的Md5
    fileMd5 = md5_cal_file(spinefile)
    # 获取配置文件md5
    confMd5 = md5_cal_file(configScale)
    if not fileMd5:
        return True
    # 第一步，检查数据库是否有记录
    dbresult = db.execute("select * from record where filepath = '%s'" % storeName).fetchone()
    # 是否重新导出
    if dbresult != None :
        if dbresult[1] == folderMd5 and dbresult[2] == fileMd5 and dbresult[3] == confMd5:
            return False
        else:
            return True
    else:
        return True

# 更新数据库内容
def db_store(path , spinefile ,configScale , storeName):
    # 得到输入目录的md5
    folderMd5 = md5_cal_folder(path)
    # 获取导出文件的Md5
    fileMd5 = md5_cal_file(spinefile)
    # 针对当前配置的Md5
    confMd5 = md5_cal_file(configScale)
    if not fileMd5:
        return False
    # 第一步，检查数据库是否有记录
    dbresult = db.execute("select * from record where filepath = '%s'" % storeName).fetchone()
    if dbresult != None :
        sql = "update record set folderMd5 = '%s' , fileMd5 = '%s' , confMd5 = '%s' where filepath = '%s'" % (folderMd5 , fileMd5 , confMd5 , storeName)
        db.execute(sql)
        db.commit()
    else:
        # 找不到记录
        sql = "insert into record values('%s', '%s' , '%s' , '%s')" % (storeName, folderMd5 , fileMd5 , confMd5)
        db.execute(sql)
        db.commit()
    return True

# 创建数据库
def db_create():
    db = sqlite3.connect(databasePath)
    db.execute('create table if not exists record (filepath varchar(1024) primary key ,folderMd5 varchar(50) , fileMd5 varchar(50) , confMd5 varchar(50) )')
    return db

################################################

# # 生成资源对应的配置文件
# def export_configFile(filename):
#     fullPath = os.path.join(config_Path,"Config")
#     if not os.path.exists(fullPath):
#         os.makedirs(fullPath)

#     fullPath = os.path.join(fullPath,"config_"+filename+".lua")
#     if not os.path.exists(fullPath):
#         fout = open(fullPath, 'w+')
#         fout.write("checkDefaul = checkDefaul or {}\n")
#         fout.write("checkDefaul[\""+filename + "\"] = true\n\n")
#         fout.write("local "+filename + " = {\n")
#         fout.write("    res = {\"spine资源\",},\n")
#         fout.write("    excute = function( ... )\n")
#         fout.write("    end,\n")
#         fout.write("}\n\n")
#         fout.write("return "+filename)
#         fout.close()

# # 生成导出成功的文件列表
# def export_sucessListFile(sucessArray):
#     fullPath = os.path.join(config_Path,"config_SucessArray.lua")
#     fout = open(fullPath, 'w+')
#     fout.write("local totalSucessArray = {\n")
#     for filename in sucessArray:
#         fout.write("    \""+filename+"\",\n")
#     fout.write("}\n")
#     fout.write("return totalSucessArray")
#     fout.close()
#     return

################################################

# 导出目录资源，并检错
def export_walkPath(folderPath , exportPath , configScale):
    # 导出文件
    print "扫描Spine文件....."

    for parent,dirnames,filenames in os.walk(folderPath):
        for filename in filenames:
            name , suffix = os.path.splitext(filename)
            if suffix == ".spine" and name == os.path.split(parent)[1]:
                # 通过文件名检查配置。
                configType = config_ignoreORspecial(name)
                exportConfig = configScale
                if type(configType) == bool:
                    if configType:
                        # 忽略表
                        print "忽略文件" + filename
                        continue
                    else:
                        # 普通导出
                        exportConfig = configScale
                else:
                    # 特殊配置
                    print "特殊导出" + filename
                    exportConfig = configType

                exportCFile = config_createNew(exportConfig)
                # 普通导出
                fullPath = os.path.join(parent,filename)
                outPutFile = os.path.join(exportPath,name + export_fileType)
                storeName = name
                # 检查是否需要重新导出
                if db_checkUpdate(parent , outPutFile , exportCFile , storeName):
                    print fullPath
                    exportFileList.append([fullPath , exportPath ,exportCFile , parent , outPutFile , storeName])

def export_allFile():
    TotalCount = 0
    SuccessCount = 0
    if len(exportFileList) > 0:
        #按字典序，避免先A12之后，再导A1会删除掉A12的图
        sortList = sorted(exportFileList,cmp = lambda x,y: cmp(os.path.split(x[0])[1],os.path.split(y[0])[1]))
        combineFile = ""
        for data in sortList:
            TotalCount += 1
            combineFile += " -i " + data[0]
            combineFile += " -o " + data[1]
            combineFile += " -e " + data[2]
        if spine_export(combineFile):
            for data in sortList:
                # 加入数据库
                if db_store(data[3] , data[4] , data[2] , data[5]):
                    SuccessCount += 1
                    print "--------------------------------"
                    print "导出文件: " + os.path.split(data[0])[1] + " 成功"
                    print "--------------------------------"
                else:
                    print "--------------------------------"
                    print "导出文件: " + os.path.split(data[0])[1] + " 加入数据库失败"
                    print "文件路径: " + fullPath
                    print "--------------------------------"
            print "共导出文件" ,TotalCount ,"个，成功",SuccessCount,"个，失败",(TotalCount-SuccessCount),"个。"
        else:
            print "--------------------------------"
            print "导出文件失败!"
            print "--------------------------------"
    else:
        print "--------------------------------"
        print "没有找到需要更新的文件!"
        print "--------------------------------"
# 错误检查
def error_checkPath(exportPath):
    # 错误文件是否齐全

    if len(faildArray) != 0:
        print "失败列表"
        print faildArray.keys()

    print "检查导出结果..."
    checkBox = {}
    for parent,dirnames,filenames in os.walk(exportPath):
        for filename in filenames:
            name , suffix = os.path.splitext(filename)
            if suffix == export_fileType:
                if checkBox.has_key(name):
                    del checkBox[name]
                else:
                    checkBox[name] = 1
            elif suffix == ".atlas":
                if checkBox.has_key(name):
                    del checkBox[name]
                else:
                    checkBox[name] = 1
    if len(checkBox) != 0:
        print "以下列表中文件资源路径设置存在问题"
        print checkBox.keys()
        exit(1)

################################################
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "请传入配置文件，格式：export.py xxxx.json"
        exit(0)
    else:
        manual_config = os.path.abspath(__file__ + "/../" + sys.argv[1])
        print "使用配置:" + manual_config

    # 检查spine版本号
    #check_version()

    # 初始化数据库地址
    databasePath = os.path.abspath(__file__ + config_getValue("dbPath"))

    # 初始化数据库
    db = db_create()

    # 读取文件格式
    export_fileType = config_getValue("exportType")

    # 初始化配置
    default_config = os.path.abspath(__file__ + config_getValue("defaultConfig"))

    # 解析数据
    for tmp in config_getValue("filePath"):
        input_res_path = os.path.abspath(__file__ + tmp["input"])
        project_Path = os.path.abspath(__file__ + tmp["output"])
        print(databasePath)
        ###########################检查执行环境################################
        if not os.path.exists(input_res_path):
            print input_res_path
            print "角色动作和特效目录不正确，请确认位置并更改脚本"
            os._exit(0)
        if not os.path.exists(spine_app_path):
            print spine_app_path
            print "spine脚本程序路径不正确，请确认位置并更改脚本"
            os._exit(0)
        if not os.path.exists(project_Path):
            print project_Path
            print "项目路径不正确，请确认位置并更改脚本"
            os._exit(0)
        if not os.path.exists(default_config):
            print default_config
            print "默认配置路径不正常，请确认位置并更改脚本"
            os._exit(0)
        if not os.path.exists(manual_config):
            print manual_config
            print "手动配置路径不正常，请确认位置并更改脚本"
            os._exit(0)

        ignoreList = tmp["ignore"]
        specialList = tmp["special"]

        export_walkPath(input_res_path , project_Path , tmp["scale"])
    print "######################################"
    export_allFile()
    #error_checkPath(project_Path)
    config_removeAllTmpFile()
    db.close()