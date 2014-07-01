#!/usr/bin/env python
#-*- coding: utf-8 -*-


from tkFileDialog import askopenfile, asksaveasfile
from tkMessageBox import askyesno


import os

########################################################################
class Dialogs(object):
    """"""

    #----------------------------------------------------------------------
    @classmethod
    def set_open_file(cls, parent, path):

        filename = askopenfile(parent=parent,
                               initialdir=path,
                               filetypes=(('Pinguino file','.pde'),('All files','*')),
                               title=os.getenv("NAME")+" - Open",
                              )

        if filename: return filename


    #----------------------------------------------------------------------
    @classmethod
    def set_save_file(cls, parent, path, filename):

        filename = asksaveasfile(parent=parent,
                                 initialdir=path,
                                 initialfile=filename,
                                 filetypes=(('Pinguino file','.pde'),('All files','*')),
                                 title=os.getenv("NAME")+" - Save",
                                )
        if filename: return filename



    #----------------------------------------------------------------------
    @classmethod
    def set_no_saved_file(cls, filename):

        return askyesno(os.getenv("NAME")+" - Save", "This file has not been saved,\nWould you like to do?\n\n"+filename[:-1])

