#!/usr/bin/env python
#-*- coding: utf-8 -*-

import webbrowser

from Tkinter import CURRENT, LEFT, BOTH


########################################################################
class PinguinoEvents(object):
    """"""


    #----------------------------------------------------------------------
    def __get_name__(self, ext=".pde"):

        index = 1
        name = "untitled-%d" % index + ext
        filenames = [self.noteBook.tab(tab)["text"] for tab in self.noteBook.tabs()]
        while name in filenames or name + "*" in filenames:
            index += 1
            name = "untitled-%d" % index + ext
        return name + "*"



    #----------------------------------------------------------------------
    def get_current_textedit(self):

        return self.Files[self.noteBook.select()]["textedit"]


    #----------------------------------------------------------------------
    def get_current_filename(self):

        return self.Files[self.noteBook.select()]["filename"]


    #----------------------------------------------------------------------
    def get_tab(self, value, fix_ouput=True):

        tab_value = self.noteBook.tab(self.noteBook.select())[value]

        if tab_value.endswith("*") and fix_ouput: return tab_value[:-1]
        else: return tab_value


    #----------------------------------------------------------------------
    def set_tab_text_changed(self, changed):

        if changed: self.noteBook.tab(self.noteBook.select(), text=self.get_tab("text") + "*")
        else: self.noteBook.tab(self.noteBook.select(), text=self.get_tab("text"))


    #----------------------------------------------------------------------
    def check_notebook_visibility(self):

        tabs = len(self.noteBook.tabs())

        if tabs > 0: self.banner.pack_forget()
        else: self.banner.pack(side=LEFT, fill=BOTH, expand=True)

    #----------------------------------------------------------------------
    def open_web_site(self, url):
        webbrowser.open_new_tab(url)