#!/usr/bin/env python
#-*- coding: utf-8 -*-


from tkFileDialog import askopenfile, asksaveasfile
from tkMessageBox import askyesno, showinfo, showwarning, showerror


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


    #----------------------------------------------------------------------
    @classmethod
    def save_before_compile(cls):

        showinfo(os.getenv("NAME")+" - Save file first", "You must save the file before compiling.")
        return True


    #----------------------------------------------------------------------
    @classmethod
    def warning_message(cls, message):

        showwarning(os.getenv("NAME") + " - Warning", message)
        return True


    #----------------------------------------------------------------------
    @classmethod
    def error_while_compiling(cls):

        showerror(os.getenv("NAME") + " - Error", "Error while compiling.")
        return True


    #----------------------------------------------------------------------
    @classmethod
    def error_while_linking(cls):

        showerror(os.getenv("NAME") + " - Error", "Error while linking.")
        return True


    #----------------------------------------------------------------------
    @classmethod
    def error_while_preprocess(cls):

        showerror(os.getenv("NAME") + " - Error", "Error while preprocess.")
        return True


    #----------------------------------------------------------------------
    @classmethod
    def error_while_unknow(cls):

        showerror(os.getenv("NAME") + " - Error", "Unknow error.")
        return True



    #----------------------------------------------------------------------
    @classmethod
    def confirm_message(cls, message):

        return askyesno(os.getenv("NAME")+" - Confirmation", message)


    #----------------------------------------------------------------------
    @classmethod
    def error_message(cls, message):

        return showerror(os.getenv("NAME")+" - Error", message)





    #----------------------------------------------------------------------
    @classmethod
    def compilation_done(cls):
        """"""
        showinfo(os.getenv("NAME")+" - Compiled", "Compilation done!")
        return True
