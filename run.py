# -*- coding: utf-8 -*-
# Author Name: Mesut Güneþ
# Author Email: gunesmes@gmail.com
# Author Github username: gunesmes

from subTranslater import SubsTranslater
import os

#set file_dir = "D:/..." the path of files to be converted
file_dir = "D:/film/sub/"

# max length of line on tv screen
# if last word left alone, it's added to the previous line
max_length = 40 

# Google can only be choosen as translator. Later, Windows and Yandex can be added.
translator = "Google"

# set languages you want to translate
target_language = "tr"
source_language = "en"


#set directory
os.chdir(file_dir)
path = os.listdir(file_dir)

s = SubsTranslater()

files = list()
for item in path:
    if item.rfind(".srt") != -1:
        files.append(item)
        continue

for i in range(len(files)):
    subFile = os.path.dirname(os.path.abspath(files[i])) +"\\" + files[i]
    
    """
    this function translate a subtitle file from original language to desired  language
    
    fileName        : names of subtitles 
    target_language : language you want to translate to
    source_language : the language of the subtitle
    translator      : Google (later Yandex, Microsoft)
    max_length      : max length of line on tv screen

    """
    
    # s.translate_substitle(fileName, target_language, source_language, translator, max_length)    
    s.translate_substitle(subFile, target_language, source_language, translator, max_length)
