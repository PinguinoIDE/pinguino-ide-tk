#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import Text, Frame

########################################################################
class Stdout(Frame, PinguinoEvents):

    def __init__(self, master=None):

        Frame.__init__(self, master)

        self.parent = master

        self.parent.geometry("640x480")
        self.parent.title(os.getenv("NAME"))