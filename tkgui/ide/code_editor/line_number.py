#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import Frame, Label, X, TOP, Text, Y, FLAT, DISABLED, END

########################################################################
class LineNumber(Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, root=None, **args):
        Frame.__init__(self, root, **args)


        #self.numbers = Label(self, bg=args["bg"], text="0")
        #self.numbers.pack(side=TOP, expand=False, fill=X)
        self.numbers = Text(self, bg=args["bg"], width=6, borderwidth=0, relief=FLAT)
        self.numbers.pack(side=TOP, fill=Y, expand=True)
        self.numbers.config(state=DISABLED)

        #self.numbers.insert(END, "HOLA")


    #----------------------------------------------------------------------
    def set_editor(self, text_edit):
        """"""
        self.textEditor = text_edit


    #def




