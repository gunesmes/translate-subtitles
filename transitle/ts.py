
# -*- coding: utf-8 -*-
# Author Name: Mesut Güneş
# Author Email: gunesmes@gmail.com
# Author Github username: gunesmes

import codecs
import sys
import time

import requests
from googletranslatepy import Translator

# get yandex translate key from: https://translate.yandex.com/developers/keys
YANDEX_API_KEY = "trnsl.YANDEX-TRANSLATE-API-KEY"
GOOGLE_TRANSLATION_LIMIT = 5000

class TranslateSubtitle():
    def __init__(self) -> None:
        pass

    @staticmethod
    def read_file_as_list(file_name):
        fr = codecs.open(file_name, "r", encoding='utf-8-sig')
        lines = fr.read()
        fr.close()
        
        # some SRTs such as created by whisper doesn't have \r\n but some other have it
        if "\r\n" in lines:
            return lines.split("\r\n\r\n")
        if "\n\n" in lines:
            return lines.split("\n\n")

    @staticmethod
    def write_file(self, file_name, target_language, source_language):
        fn = self.format_file_name(file_name, target_language, source_language)
        fw = open(fn, 'w')

        return fw

    @staticmethod
    def format_file_name(file_name, target_language, source_language):
        name_sep = "_" + source_language + "_to_" + target_language

        # index number of last dot
        last_dot = file_name.rfind('.')

        # means that there is no dot in the file name, 
        # and file name has no file type extension 
        if last_dot == -1:
            new_file_name = file_name + str(name_sep) + '.srt'

        else:
            baseName = file_name[0: last_dot]
            ext = file_name[last_dot: len(file_name)]
            new_file_name = baseName + str(name_sep) + ext
        return new_file_name

    @staticmethod
    def yandex_translator(prepared_sub, source_language, target_language):
        # Using Yandex translator api is free!
        url = "https://translate.yandex.net/api/v1.5/tr.json/translate"

        # Get Yandex API key from http://api.yandex.com/key/form.xml?service=trnsl
        yandex_api_key = YANDEX_API_KEY

        data = {
            'text': prepared_sub,
            'format': "plain",
            'lang': source_language + "-" + target_language,
            'key': yandex_api_key
        }

        response = requests.post(url, data)
        response = response.json()
        if response["code"] > 400:
            print(
                "\n   Get Yandex API key from 'http://api.yandex.com/key/form.xml?service=trnsl' \n   then set the 'yandex_api_key' at line 100 in 'src/subtitle_translater.py'\n")
            sys.exit()

        return response['text'][0]


    def subtitle_translator(self, file_name, translator_tool, source_language, target_language):
        """
        this function translate a subtitle file from original language to desired  language
        
        line may be the order number of the subtitle or just for real line 
        such as answer to age given "33" or there is no order number but "-->"   
        must be present to in the middle of the start and end time of subtitle
        to be shown. There must a empty line between two ordered subtitle.
        Expected / standart subtitle should be like this:    
            1
            00:00:27,987 --> 00:00:29,374
            - Babe.
            - Mmm.
            
            2
            00:00:30,210 --> 00:00:31,634
            - Lizzie.
            - Mmm.
            
            3
        """
        fw = self.write_file(self, file_name, target_language, source_language)
        content_list = self.read_file_as_list(file_name)
        durations = []
        contents = []
        text_translatable = ''
        translator = Translator(source=source_language, target=target_language)
        number_of_translatable_content = len(content_list)

        for c in range(number_of_translatable_content):
            lines = []
            # some SRTs such as created by whisper doesn't have \r\n but some other have it
            if "\r\n" in content_list[c]:
                lines = content_list[c].split("\r\n")
            if "\n" in content_list[c]:
                lines = content_list[c].split("\n")

            time_info = ''
            text_info = ''
            for i in range(len(lines)):
                if lines[i].rstrip().isdigit() and "-->" in lines[i + 1] or "-->" in lines[i]:
                    time_info += lines[i] + "\r\n"
                    continue
                else:
                    text_info += lines[i] + "\n" 
                
            # list doesn't have the value at number_of_translatable_content index
            if len(text_translatable) + len(text_info) > GOOGLE_TRANSLATION_LIMIT or c == number_of_translatable_content-1:
                try:  
                    translated_sub = translator.translate(text_translatable)
                    # translated_sub = self.yandex_translator(text_translatable, source_language, target_language)
                    temp_translated = translated_sub.split("\n\r")
                    temp_translated[-1] = temp_translated[-1] + "\n"
                    contents += temp_translated
                except TypeError as err:
                    translated_sub = 'err'
                    print(err)
                    
                text_translatable = text_info
                time.sleep(5)
            else:
                durations.append(time_info)
                text_translatable += text_info + "\n\r"
                
        for d, c in zip(durations, contents):
            fw.write(d)
            fw.write(c + "\n")
            print(d + c)

        # Print information about the subtitle
        info = "Translated by subtitle_translator via %s translator \nwritten by Mesut Gunes: https://github.com/gunesmes/subtitle_translator\n" % translator_tool
        fw.write(info)
        print(info)
        print("New file name: ", self.format_file_name(file_name, target_language, source_language))
