#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from PIL import ImageTk

from Tkinter import Text, Button, Frame, END, FLAT, LEFT, Y, X, CURRENT, SEL_FIRST, SEL_LAST, INSERT, GROOVE

from ..code_editor.pinguino_code_editor import PinguinoCodeEditor
from ..methods.methods import PinguinoEvents
from ..methods.dialogs import Dialogs
from ..methods.decorators import Decorator


########################################################################
class PinguinoEvents(PinguinoEvents):

    #----------------------------------------------------------------------
    def connect_events(self):

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

                        #("edit-find", self.new_file),
                        #("edit-find-replace", self.new_file),

                        #("separator", None),

                        ("applications-electronics", self.__show_board_config__),
                        ("system-run", self.pinguino_compile),
                        ("emblem-downloads", self.pinguino_upload),
                        ]

        for icon, function in toolbar_icons:

            if icon == "separator":
                frame = Frame(self.toolBar, width=10)
                frame.pack(side=LEFT, fill=Y, padx=2, pady=2)

            else:
                icon = os.path.join("tkgui", "resources", "themes", "pinguino11", icon+".png")
                #eimg = ImageTk.PhotoImage(Image.open(icon))
                eimg = ImageTk.PhotoImage(file=icon)

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
        textedit.update_syntax()
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
        textedit.update_syntax()
        self.noteBook.add(frame_edit, text=os.path.split(filename)[-1])

        self.noteBook.select(self.noteBook.tabs()[-1])
        self.Files[self.noteBook.select()] = {}
        self.Files[self.noteBook.select()]["textedit"] = textedit
        self.Files[self.noteBook.select()]["filename"] = filename
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
            return True
        return False


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

        self.Files.pop(self.noteBook.select())
        self.noteBook.deletecommand(self.noteBook.select())
        self.check_notebook_visibility()



    #----------------------------------------------------------------------
    def close_all(self, event=None):

        while len(self.noteBook.tabs()) > 0:
            self.close_file()


    #----------------------------------------------------------------------
    def close_ide(self, event=None):

        self.master.destroy()


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



    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    @Decorator.requiere_file_saved()
    @Decorator.requiere_can_compile()
    def pinguino_compile(self, event=None):

    ##----------------------------------------------------------------------
    #def pinguino_compile(self, dialog_upload=True):

        filename = self.get_current_filename()
        compile_code = lambda :self.pinguinoAPI.compile_file(filename)

        self.set_board()
        #reply = Dialogs.confirm_board(self)
        #if reply == False:
            #self.__show_board_config__()
            #return False
        #elif reply == None:
            #return False

        self.write_log("compilling: %s"%filename)
        self.write_log(self.get_description_board())
        self.write_log("")

        compile_code()
        self.post_compile()


    #----------------------------------------------------------------------
    def post_compile(self):

        #self.main.actionUpload.setEnabled(self.pinguinoAPI.compiled())
        if not self.pinguinoAPI.compiled():

            errors_preprocess = self.pinguinoAPI.get_errors_preprocess()
            if errors_preprocess:
                for error in errors_preprocess["preprocess"]:
                    self.write_log("ERROR: "+error)

            errors_c = self.pinguinoAPI.get_errors_compiling_c()
            if errors_c:
                self.write_log("ERROR: "+errors_c["complete_message"])
                line_errors = errors_c["line_numbers"]
                for line_error in line_errors:
                    self.highligh_line(line_error, "#ff7f7f")

            errors_asm = self.pinguinoAPI.get_errors_compiling_asm()
            if errors_asm:
                for error in errors_asm["error_symbols"]:
                    self.write_log("ERROR: "+error)

            errors_linking = self.pinguinoAPI.get_errors_linking()
            if errors_linking:
                for error in errors_linking["linking"]:
                    self.write_log("ERROR: "+error)

                line_errors_l = errors_linking["line_numbers"]
                for line_error in line_errors_l:
                    self.highligh_line(line_error, "#ff7f7f")


            if errors_asm or errors_c:
                if Dialogs.error_while_compiling():
                    self.__show_stdout__()
            elif errors_linking:
                if Dialogs.error_while_linking():
                    self.__show_stdout__()
            elif errors_preprocess:
                if Dialogs.error_while_preprocess():
                    self.__show_stdout__()

            else:
                if Dialogs.error_while_unknow():
                    self.__show_stdout__()

        else:
            result = self.pinguinoAPI.get_result()
            self.write_log("compilation done")
            self.write_log(result["code_size"])
            self.write_log("%s seconds process time"%result["time"])


            Dialogs.compilation_done()


    #----------------------------------------------------------------------
    def highligh_line(self, line, color):
        """"""

    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def pinguino_upload(self, event=None):
        uploaded, result = self.pinguinoAPI.upload()
        self.write_log(result)
        if uploaded:
            Dialogs.upload_done()
        elif Dialogs.upload_fail(result):
            self.pinguino_upload()



    #----------------------------------------------------------------------
    def get_description_board(self):

        board = self.pinguinoAPI.get_board()
        board_config = "Board: %s\n" % board.name
        board_config += "Proc: %s\n" % board.proc
        board_config += "Arch: %d\n" % board.arch

        if board.arch == 32:
            board_config += "MIPS 16: %s\n" % str(self.configIDE.config("Board", "mips16", True))
            board_config += "Heap size: %d bytes\n" % self.configIDE.config("Board", "heapsize", 512)
            board_config += "Optimization: %s\n" % self.configIDE.config("Board", "optimization", "-O3")

        if board.arch == 8 and board.bldr == "boot4":
            board_config += "Boootloader: v4\n"
        if board.arch == 8 and board.bldr == "boot2":
            board_config += "Boootloader: v1 & v2\n"

        return board_config