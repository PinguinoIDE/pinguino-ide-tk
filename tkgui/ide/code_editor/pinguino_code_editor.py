#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import Frame, RIGHT, LEFT, BOTH, X, Y, Scrollbar, BOTTOM, FLAT

from tkgui.ide.code_editor.line_number import LineNumber
from tkgui.ide.code_editor.editor import PinguinoTextEdit

########################################################################
class PinguinoCodeEditor(Frame):

    #----------------------------------------------------------------------
    def __init__(self, root=None):

        Frame.__init__(self, root)

        self.textedit = PinguinoTextEdit(self, borderwidth=0, relief=FLAT, highlightthickness=0, font="mono 11")

        self.linenumber = LineNumber(self, bg="#afc8e1", borderwidth=0, relief=FLAT, highlightthickness=0)
        self.linenumber.set_editor(self.textedit)
        self.textedit.set_linenumber(self.linenumber)

        ysb = Scrollbar(self.textedit, orient='vertical', command=self.textedit.yview)
        xsb = Scrollbar(self.textedit, orient='horizontal', command=self.textedit.xview)

        self.textedit.set_scrolls(xsb, ysb)

        self.textedit.configure(yscroll=ysb.set, xscroll=xsb.set)


        xsb.pack(side=BOTTOM, fill=X, expand=False)
        ysb.pack(side=RIGHT, fill=Y, expand=False)

        self.textedit.pack(side=RIGHT, fill=BOTH, expand=True)
        self.linenumber.pack(side=LEFT, fill=Y, expand=False)

        Frame(self, bg="#e7e7e7", width=10).pack(side=LEFT, fill=Y)
        Frame(self, bg="#ffffff", width=5).pack(side=LEFT, fill=Y)

        ysb.bind("<B1-Motion>", self.textedit.update_linenumber)
        self.textedit.bind("<B1-Motion>", self.textedit.update_linenumber)
        self.textedit.bind("<Button-4>", self.textedit.update_linenumber)
        self.textedit.bind("<Button-5>", self.textedit.update_linenumber)
        self.textedit.bind("<MouseWheel>", self.textedit.update_linenumber)
