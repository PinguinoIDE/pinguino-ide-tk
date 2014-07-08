#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

from Tkinter import Text, Frame, BOTH, Scrollbar, TOP, BOTTOM, RIGHT, X, Y, INSERT, Button


########################################################################
class Stdout(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.parent = master

        self.parent.geometry("640x480")
        self.parent.title(os.getenv("NAME"))

        self.textedit = Text(self.parent, font="mono 10")
        self.textedit.pack(expand=True, fill=BOTH)
        buton = Button(self.parent, text="Close", command=self.quit)
        buton.pack(side=RIGHT, expand=False, padx=10, pady=10, ipadx=10)

        ysb = Scrollbar(self.textedit, orient='vertical', command=self.textedit.yview)
        xsb = Scrollbar(self.textedit, orient='horizontal', command=self.textedit.xview)

        self.textedit.configure(yscroll=ysb.set, xscroll=xsb.set)

        xsb.pack(side=BOTTOM, fill=X, expand=False)
        ysb.pack(side=RIGHT, fill=Y, expand=False)

        self.textedit.pack(side=TOP, fill=BOTH, expand=True)


        self.show_file()



    #----------------------------------------------------------------------
    def show_file(self):

        PINGUINO_STDOUT_FILE = os.path.join(os.getenv("PINGUINO_USER_PATH"), "source", "stdout")
        file = open(PINGUINO_STDOUT_FILE, "r")
        self.textedit.insert(INSERT, "".join(file.readlines()))
        file.close()



    #----------------------------------------------------------------------
    def quit(self):
        """"""
        self.master.destroy()