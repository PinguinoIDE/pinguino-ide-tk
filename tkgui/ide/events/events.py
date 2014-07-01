#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
from datetime import datetime

from Tkinter import Text, Button, Frame, END, FLAT, LEFT, Y, X, CURRENT, SEL_FIRST, SEL_LAST, INSERT, GROOVE

from PIL import Image, ImageTk
from ..code_editor.pinguino_code_editor import PinguinoCodeEditor
from ..methods.methods import PinguinoEvents
from ..methods.dialogs import Dialogs


########################################################################
class PinguinoEvents(PinguinoEvents):
    """"""

    #----------------------------------------------------------------------
    def connect_events(self):
        """"""

        toolbar_icons = [("document-new", self.new_file),
                        ("document-open", self.open_file),
                        ("document-save", self.save_file),

                        ("separator", None),

                        ("edit-undo", self.edit_undo),
                        ("edit-redo", self.edit_redo),

                        ("separator", None),

                        ("edit-cut", self.edit_cut),
                        ("edit-copy", self.edit_copy),
                        ("edit-paste", self.edit_paste),

                        ("separator", None),

                        ("edit-find", self.new_file),
                        ("edit-find-replace", self.new_file),

                        ("separator", None),

                        ("applications-electronics", self.new_file),
                        ("system-run", self.new_file),
                        ("emblem-downloads", self.new_file),
                        ]

        for icon, function in toolbar_icons:

            if icon == "separator":
                frame = Frame(self.toolBar, width=10)
                frame.pack(side=LEFT, fill=Y, padx=2, pady=2)

            else:
                icon = os.path.join("tkgui", "resources", "themes", "pinguino11", icon+".png")
                eimg = ImageTk.PhotoImage(Image.open(icon))

                button = Button(self.toolBar, image=eimg, relief=FLAT, command=function, borderwidth=0, highlightthickness=0)
                button.image = eimg
                button.pack(side=LEFT, padx=2, pady=4)



    #----------------------------------------------------------------------
    def new_file(self, event=None):

        today = datetime.now()
        minimun = "void setup() {\n\t// put your setup code here, to run once:\n\n\t\n}\n\nvoid loop() {\n\t// put your main code here, to run repeatedly:\n\n}\n"
        file_= """/*-----------------------------------------------------
%s:  --<>
%s: %s
%s:

-----------------------------------------------------*/
        """ %("Author", "Date", today.strftime("%Y-%m-%d"), "Description")

        minimun = minimun.replace("\t", " "*4)
        file_ = file_.replace("\t", " "*4)

        filename = self.__get_name__()
        frame_edit = PinguinoCodeEditor(self)
        textedit = frame_edit.textedit
        textedit.insert(END, file_ + "\n\n" + minimun)
        self.noteBook.add(frame_edit, text=filename)

        #tab = self.noteBook.tab(self.noteBook.tabs()[-1])

        self.noteBook.select(self.noteBook.tabs()[-1])
        self.Files[self.noteBook.select()] = {}
        self.Files[self.noteBook.select()]["textedit"] = textedit
        self.Files[self.noteBook.select()]["filename"] = None

        self.check_notebook_visibility()



    #----------------------------------------------------------------------
    def open_file(self, filename=None):

        if filename is None:
            file = Dialogs.set_open_file(self, "/home/yeison/Escritorio")
            if file is None: return
        else: file = open(filename, "r")

        filename = file.name
        content = "".join(file.readlines())
        file.close()
        frame_edit = PinguinoCodeEditor(self)
        textedit = frame_edit.textedit
        textedit.insert(END, content)
        self.noteBook.add(frame_edit, text=os.path.split(filename)[-1])

        #tab = self.noteBook.tab(self.noteBook.tabs()[-1])

        self.noteBook.select(self.noteBook.tabs()[-1])
        self.Files[self.noteBook.select()] = {}
        self.Files[self.noteBook.select()]["textedit"] = textedit
        self.Files[self.noteBook.select()]["filename"] = filename

        #self.Files[self.noteBook.tabs()[-1].id] = textedit
        #setattr(textedit, "filename", filename)

        self.check_notebook_visibility()


    #----------------------------------------------------------------------
    def save_file(self, event=None):

        textedit = self.get_current_textedit()
        filename = self.get_current_filename()
        if filename: file = open(filename, "w")
        else:  file = Dialogs.set_save_file(self, "/home/yeison/Escritorio", self.get_tab("text"))
        if file:
            self.set_tab_text_changed(False)
            self.Files[self.noteBook.select()]["filename"] = file.name
            self.parent.title(os.getenv("NAME")+" - "+file.name)
            file.writelines(textedit.get("0.0", END))
            file.close()


    #----------------------------------------------------------------------
    def save_as(self, event=None):

        textedit = self.get_current_textedit()
        file = Dialogs.set_save_file(self, "/home/yeison/Escritorio", self.get_tab("text"))
        if file:
            self.set_tab_text_changed(False)
            self.Files[self.noteBook.select()]["filename"] = file.name
            self.parent.title(os.getenv("NAME")+" - "+file.name)
            self.noteBook.tab(self.noteBook.select(), text=os.path.split(file.name)[1])
            file.writelines(textedit.get("0.0", END))
            file.close()


    #----------------------------------------------------------------------
    def close_file(self, event=None):

        if self.get_tab("text", False).endswith("*"):
            if Dialogs.set_no_saved_file(self.get_tab("text")):
                self.save_file()

        self.noteBook.deletecommand(self.noteBook.select())
        self.check_notebook_visibility()



    #----------------------------------------------------------------------
    def close_all(self, event=None):

        while len(self.noteBook.tabs()) > 0:
            self.close_file()


    #----------------------------------------------------------------------
    def close_ide(self, event=None):
        sys.exit(0)


    #----------------------------------------------------------------------
    def edit_undo(self, event=None):

        textedit = self.get_current_textedit()
        textedit.edit_undo()
        pass


    #----------------------------------------------------------------------
    def edit_redo(self, event=None):

        textedit = self.get_current_textedit()
        textedit.edit_redo()


    #----------------------------------------------------------------------
    def edit_cut(self, event=None):

        self.edit_copy()
        textedit = self.get_current_textedit()
        textedit.delete(SEL_FIRST, SEL_LAST)


    #----------------------------------------------------------------------
    def edit_copy(self, event=None):

        textedit = self.get_current_textedit()
        text = textedit.get(SEL_FIRST, SEL_LAST)
        textedit.clipboard_clear()
        textedit.clipboard_append(text)


    #----------------------------------------------------------------------
    def edit_paste(self, event=None):

        textedit = self.get_current_textedit()
        textedit.selection_clear()
        text = textedit.selection_get(selection='CLIPBOARD')
        textedit.insert(INSERT, text)
