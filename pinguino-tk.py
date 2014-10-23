#!/usr/bin/python2
#-*- coding: utf-8 -*-

NAME = "Pinguino IDE tk"
VERSION = "11.0"
SUBVERSION = "beta.1"
#DESCRIPTION = ""
#LONG_DESCRIPTION = ""

################################################################################

"""-------------------------------------------------------------------------
    Pinguino IDE tk

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
-------------------------------------------------------------------------"""

################################################################################

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os

import debugger
debugger.Debugger(sys, clear=True)

os.environ["NAME"] = NAME
os.environ["VERSION"] = VERSION
os.environ["SUBVERSION"] = SUBVERSION
os.environ["PINGUINO_HOME"] = os.path.abspath(sys.path[0])

# For PyInstaller compatibility
if os.path.exists(os.path.abspath("pinguino_data")):
    os.environ["PINGUINO_DATA"] = os.path.abspath("pinguino_data")
else:
    os.environ["PINGUINO_DATA"] = os.getenv("PINGUINO_HOME")

import argparse
from tkgui.pinguino_api.boards import boardlist

#----------------------------------------------------------------------
def build_argparse():

    parser = argparse.ArgumentParser(description="*** %s ***"%os.getenv("NAME"))
    parser.add_argument("-v", "--version", dest="version", action="store_true", default=False, help="show %s version and exit"%os.getenv("NAME"))
    parser.add_argument("-a", "--author", dest="author", action="store_true", default=False, help="show authors of this %s version and exit"%os.getenv("NAME"))
    parser.add_argument("-f", "--filename", dest="filename", nargs=1, default=False, help="filename to process")
    parser.add_argument("-l", "--boot", dest="bootloader", nargs=1, default=False, help="set bootloader option")
    parser.add_argument("-x", "--upload", dest="upload", action="store_true", default=False, help="upload code")
    parser.add_argument("-g", "--hex", dest="hex_file", action="store_true", default=False, help="print hex_file")

    for board in boardlist:
        parser.add_argument(board.shortarg, board.longarg, dest="board", const=board, action="store_const", default=False,
                            help="compile code for " + board.board + " board")

    return parser.parse_args()

try:
    parser = build_argparse()
    parser_state = True
except:
    parser_state = False


if __name__ == "__main__":

    #sys.path.append(os.path.join(os.getenv("PINGUINO_DATA"), "qtgui", "resources"))

    python_path_modules = os.path.join(os.getenv("PINGUINO_DATA"), "python_requirements")
    if os.path.isdir(python_path_modules): sys.path.append(python_path_modules)

    if len(sys.argv) == 1 or not parser_state:

        from Tkinter import Tk
        from tkgui.ide import PinguinoIDE

        root = Tk()

        #icon = os.path.join("tkgui", "resources", "art", "pinguino11.ico")
        #root.iconbitmap(icon)
        #root.tk.call('wm', 'iconbitmap', self._w, '-default', 'pinguino11.ico')


        app = PinguinoIDE(master=root)

        #app.parent.configure(background = 'red')
        app.mainloop()
        #root.destroy()


    elif parser_state:  #command line

        from tkgui.pinguino_api.pinguino import Pinguino
        from tkgui.pinguino_api.pinguino_config import PinguinoConfig
        from tkgui.ide.methods.config import Config

        pinguino = Pinguino()
        PinguinoConfig.set_environ_vars()
        PinguinoConfig.check_user_files()
        config = Config()
        PinguinoConfig.update_pinguino_paths(config, Pinguino)
        PinguinoConfig.update_pinguino_extra_options(config, Pinguino)
        PinguinoConfig.update_user_libs(pinguino)

        #parser = pinguino.build_argparse()

        if parser.version:
            print("\t" + VERSION)
            sys.exit()

        if parser.author:
            print("\tJean-Pierre Mandon")
            print("\tRegis Blanchot")
            print("\tYeison Cardona")
            sys.exit()

        if parser.board:
            pinguino.set_board(parser.board)
            print("using %s board" % parser.board.name)

            if parser.bootloader:
                bootloader = pinguino.dict_boot.get(parser.bootloader[0].lower(), parser.board.bldr)
                pinguino.set_bootloader(bootloader)
            print("using %s bootloader" % pinguino.get_board().bldr)

            if not parser.filename:
                print("ERROR: missing filename")
                sys.exit(1)

            else:
                filename = parser.filename[0]

                fname, extension = os.path.splitext(filename)
                if extension != ".pde":
                    print("ERROR: bad file extension, it should be .pde")
                    sys.exit()
                del fname, extension

                pinguino.compile_file(filename)

                if not pinguino.compiled():
                    print("\nERROR: no compiled\n")

                    errors_proprocess = pinguino.get_errors_preprocess()
                    if errors_proprocess:
                        for error in errors_proprocess["preprocess"]: print(error)

                    errors_c = pinguino.get_errors_compiling_c()
                    if errors_c:
                        print(errors_c["complete_message"])

                    errors_asm = pinguino.get_errors_compiling_asm()
                    if errors_asm:
                        for error in errors_asm["error_symbols"]: print(error)

                    errors_link = pinguino.get_errors_linking()
                    if errors_link:
                        for error in errors_link["linking"]: print(error)

                    sys.exit()

                else:
                    result = pinguino.get_result()
                    print("compilation time: %s" % result["time"])
                    print("compiled to: %s" % result["hex_file"])

                    if parser.hex_file:
                        hex_file = open(result["hex_file"], "r")
                        content_hex = hex_file.readlines()
                        hex_file.close()
                        print("\n" + "*" * 70)
                        print(result["hex_file"])
                        print("*" * 70)
                        for line in content_hex: print(line),
                        print("*" * 70 + "\n")

                if parser.upload:
                    try:
                        uploaded, result = pinguino.upload()
                        if result:
                            print(result)
                    except:
                        if pinguino.get_board().arch == 8:
                            print("ERROR: is possible that a parameter is incorrect, try another bootloader option.")
                            print("Boloader options: "),
                            print(", ".join(pinguino.dict_boot.keys()))
