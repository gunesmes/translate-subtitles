# -*- coding: utf-8 -*-
# Author Name: Mesut Güneþ
# Author Email: gunesmes@gmail.com
# Author Github username: gunesmes

from subTranslater import SubsTranslater
import os, sys, getopt


def translater(argv):
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "options")
    except getopt.GetoptError, err:
      print err
      sys.exit(2)

    try:
        #set file_dir = "D:/..." the path of files to be converted
        #file_dir = "/Users/mesutgunes/Projects/subtitle_translator"
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
        print "Arguments Error! Please run the file with the following format:" 
        print "\n   python run.py 'path/to/files' 'max-length-of-lines' 'translator:google or yandex' 'source language' 'target language'\n   python run.py /Users/mesutgunes/Projects/subtitle_translator 40 google pl tr\n"
        sys.exit(2)

    #set directory
    os.chdir(file_dir)
    path = os.listdir(file_dir)

    s = SubsTranslater()

    # get the .srt files from the dir
    files = list()
    for item in path:
        if item.rfind(".srt") != -1:
            files.append(item)
            continue

    for i in range(len(files)):
        subFile = os.path.dirname(os.path.abspath(files[i])) +"/" + files[i]
        
        """
        this function translate a subtitle file from original language to desired  language
        
        fileName        : names of subtitles 
        target_language : language you want to translate to
        source_language : the language of the subtitle
        translator      : Google (later Yandex, Microsoft)
        max_length      : max length of line on tv screen

        """
        
        # s.translate_substitle(fileName, target_language, source_language, translator, max_length)    
        s.translate_substitle(subFile, source_language, target_language, translator, max_length)


if __name__ == "__main__":
   translater(sys.argv[1:])
