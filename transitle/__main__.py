# -*- coding: utf-8 -*-
# Author Name: Mesut Güneş
# Author Email: gunesmes@gmail.com
# Author GitHub username: gunesmes

import getopt
import os
import sys
from datetime import datetime
from .translator import ts

sys.path.append("src")


def main():
    args = sys.argv
    print(args[1:])

    try:
        optlist, args = getopt.getopt(sys.argv[1:], "options")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    try:
        # set file_dir = "D:/..." the path of files to be converted
        # file_dir = "/Users/mesutgunes/Projects/subtitle_translator"
        file_dir = args[0]

        # Google can only be choosen as translator. Later, Windows and Yandex can be added.
        translator = args[1]

        # set languages you want to translate
        source_language = args[2]
        target_language = args[3]
    except IndexError:
        print("Arguments Error! Please run the file with the following format:")
        print(
            "\n   ts 'path/to/files' 'translator:google or yandex' 'source language' 'target language'\n   ts /Users/mesutgunes/Downloads/subtitles google pl tr\n")
        sys.exit(2)

    ts(file_dir=file_dir, translator=translator, source_lang=source_language, target_lang=target_language)