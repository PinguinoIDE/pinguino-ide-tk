#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os
import sys

files = filter(lambda f:f.endswith(".svg"), os.listdir(sys.path[0]))
size = 32

for file in files:
    os.system("inkscape -z -e %s -w %d -h %d %s" % (file.replace(".svg",".png"), size, size, file))


