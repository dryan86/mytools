#!/usr/bin/env python
#encoding:utf8

import os
import os.path
import re


def getSpineVersion():
	p = re.compile(r'Spine (?:[0-9.]*) Professional, JGLFW')


	# 检查spine的版本号
	command = "/Applications/Spine/Spine.app/Contents/MacOS/Spine --version"

	output = os.popen(command)
	res = output.read()


	versionStr = p.findall(res)[0]

	return versionStr

def checkIsVersion(ver):
	curVersion = getSpineVersion()

	p2 = re.compile(r'' + ver)

	# 判断是否是ver
	version = p2.findall(curVersion)

	if len(version) > 0:
		return True
	else:
		return False


# print checkIsVersion("2.1.27")