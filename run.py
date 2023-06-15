# -*- coding: utf-8 -*-
# Author Name: Mesut Güneş
# Author Email: gunesmes@gmail.com
# Author GitHub username: gunesmes

import getopt
import os
import sys
from datetime import datetime

sys.path.append("src")

from subtitle_translater import SubsTranslater


def translater(argv):
    start_time = datetime.now()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "options")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    try:
        # set file_dir = "D:/..." the path of files to be converted
        # file_dir = "/Users/mesutgunes/Projects/subtitle_translator"
        file_dir = args[0]

        # max length of line on tv screen
        # if last word left alone, it's added to the previous line
        max_length = int(args[1])

        # Google can only be choosen as translator. Later, Windows and Yandex can be added.
        translator = args[2]

        # set languages you want to translate
        source_language = args[3]
        target_language = args[4]
    except IndexError:
        print("Arguments Error! Please run the file with the following format:")
        print(
            "\n   python run.py 'path/to/files' 'max-length-of-lines' 'translator:google or yandex' 'source language' 'target language'\n   python run.py /Users/mesutgunes/Projects/subtitle_translator 40 google pl tr\n")
        sys.exit(2)

    # set directory
    os.chdir(file_dir)
    path = os.listdir(file_dir)

    s = SubsTranslater()

    # get the .srt files from the dir
    files = list()
    for item in path:
        if item.rfind(".srt") != -1:
            files.append(item)
            continue

    for file in files:
        print(f" - - - - Translating: {file} - - - - - -")
        subFile = os.path.dirname(os.path.abspath(file)) + "/" + file

        """
        this function translate a subtitle file from original language to desired  language
        
        fileName        : names of subtitles 
        target_language : language you want to translate to
        source_language : the language of the subtitle
        translator      : Google (later Yandex, Microsoft)
        max_length      : max length of line on tv screen

        """

        s.translate_subtitle_raw(subFile, source_language, target_language, translator, max_length)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

if __name__ == "__main__":
    translater(sys.argv[1:])
