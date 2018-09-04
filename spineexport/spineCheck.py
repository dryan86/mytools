# !/usr/bin/env python3
# -*- coding:utf-8 -*-
'check spine filename module'
import os
import sys
__normal = True #检测标记

# 处理spine文件及其资源
def __dealSpineFile(fileDict, resList):
	for name, infolist in fileDict.items():
		if infolist[0] > 1:
			print("[%s]重复次数为: %d ,所在目录路径:" % (name + ".spine", infolist[0]))
			for path in infolist[1:]:
				print("    => " + path)

	if len(resList):
		print("下列资源文件存在命名有空格问题：")
		for resName in resList:
			print("    => " + resName)

# 处理导出目录中的问题
def __dealOutputFile(needlessList):
	if len(needlessList):
		print("在导出目录下有未清理文件:")
		for fileName in needlessList:
			if fileName[-1:] == "l":
				print("    => " + fileName + ".png.atlas")
			else:
				print("    => " + fileName)

# 搜索所有后缀为spine的文件
def searchSpineFiles(aeDir, outputDir):
	global __normal
	# spine文件字典
	spineFileDict = {}
	# 命名中有空格的文件列表
	errorResList = []
	# 处理AE目录
	for curDirPath, dirList, fileList in os.walk(aeDir):
		curDirPath = curDirPath[(curDirPath.find("AE") + len("AE") + 1):]
		for fileName in fileList:
			name, postfix = os.path.splitext(fileName)
			if postfix == ".spine":
				if name != os.path.split(curDirPath)[1]:
					__normal = False
					print("[%s]目录 存在命名问题" % curDirPath)
					# exit(0)
				if not name in spineFileDict:
					spineFileDict[name] = []
					spineFileDict[name].append(1) # 重复次数
				else:
					__normal = False
					spineFileDict[name][0] += 1
				spineFileDict[name].append(curDirPath) # 重复问题出现的目录
			elif postfix in set([".png", ".jpg"]):
				if name.find(" ") != -1: # 判断是否有空格存在
					__normal = False
					errorResList.append(curDirPath + "/" + fileName)
	__dealSpineFile(spineFileDict, errorResList)
	# 处理导出目录
	needlessList = [] # 多余的文件列表
	for curDirPath, dirList,fileList in os.walk(outputDir):
		for fileName in fileList:
			name, postfix = os.path.splitext(fileName)
			# 在animation中三者为一套[".atlas", ".png", ".skel"]
			if postfix in set([".skel", ".event"]):
				if not name in spineFileDict:
					__normal = False
					needlessList.append(fileName)
	__dealOutputFile(needlessList)

	if __normal:
		print("--------------------")
		print("检查完毕, 一切正常!")
		print("--------------------")
	else:
		print("------------------------")
		print("检测出异常, 请及时修改!")
		print("------------------------")
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        print("#######################################")
        aeDir = sys.argv[1] + "/AE"
        outputDir = sys.argv[1] + "/Output"
        print("AE目录为 : %s" % aeDir)
        print("导出目录为: %s" % outputDir)
        print("---------------------------------------")
        searchSpineFiles(aeDir, outputDir)
    else:
        print("请先设置检查目录与导出目录......")
        exit(0)
