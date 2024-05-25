
# -*- coding: utf-8 -*-
# Author Name: Mesut Güneş
# Author Email: gunesmes@gmail.com
# Author Github username: gunesmes

import codecs
import os
import time
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator)

TRANSLATION_LIMIT = 5000

class TranslateSubtitle():
    def __init__(self, abs_path, out, translator, source_lang, target_lang) -> None:
        self.abs_path = abs_path
        self.translation_path = out
        self.translator = translator
        self.source_lang = source_lang
        self.target_lang = target_lang

    def read_file_as_list(self, file_name):
        fr = codecs.open(file_name, "r", encoding='utf-8-sig')
        lines = fr.read()
        fr.close()
        
        # some SRTs such as created by whisper doesn't have \r\n but some other have it
        if "\r\n" in lines:
            return lines.split("\r\n\r\n")
        if "\n\n" in lines:
            return lines.split("\n\n")

    def write_file(self, file_name):
        fn = self.format_file_name(file_name)
        fw = open(fn, 'w')
        return fw

    def format_file_name(self, file_name):
        # Check if the directory already exists
        if not os.path.exists(self.translation_path):
            # If it doesn't exist, create the directory
            os.makedirs(self.translation_path)
            print(f"Translation folder created at: {self.translation_path}")

        name_sep = f'{self.source_lang}-to-{self.target_lang}-{self.translator}'

        # index number of last dot
        last_dot = file_name.rfind('.')

        # means that there is no dot in the file name, 
        # and file name has no file type extension 
        if last_dot == -1:
            new_file_name = self.translation_path + file_name + str(name_sep) + '.srt'
        else:
            baseName = file_name[0: last_dot]
            ext = file_name[last_dot: len(file_name)]
            new_file_name = self.translation_path + baseName + str(name_sep) + ext
        return new_file_name

    def subtitle_translator(self, file_name):
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
        fw = self.write_file(file_name)
        content_list = self.read_file_as_list(file_name)
        durations = []
        contents = []
        text_translatable = ''
        
        translator = None
        if self.translator == 'google':
            translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)

        if self.translator == 'chatgpt':
            translator = ChatGptTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'microsoft':
            translator = MicrosoftTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'pons':
            translator = PonsTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'linguee':
            translator = LingueeTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'mymemory':
            translator = MyMemoryTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'yandex':
            translator = YandexTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'papago':
            translator = PapagoTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'deepl':
            translator = DeeplTranslator(source=self.source_lang, target=self.target_lang)
        
        if self.translator == 'qcri':
            translator = QcriTranslator(source=self.source_lang, target=self.target_lang)
                
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
                if i < len(lines) - 1 and lines[i].rstrip().isdigit() and "-->" in lines[i + 1] or "-->" in lines[i]:
                    time_info += lines[i] + "\r\n"
                    continue
                else:
                    text_info += lines[i] + "\n" 
                
            # list doesn't have the value at number_of_translatable_content index
            if len(text_translatable) + len(text_info) > TRANSLATION_LIMIT or c == number_of_translatable_content-1:
                try:  
                    translated_sub = translator.translate(text_translatable)
                    # translated_sub = self.yandex_translator(text_translatable, self.source_lang, self.target_lang)
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
            fw.write(d.replace('\r\r', ''))
            fw.write(c + "\n")
            print(d + c)

        # Print information about the subtitle
        info = "Translated by subtitle_translator via %s translator \nwritten by Mesut Gunes: https://github.com/gunesmes/subtitle_translator\n" % self.translator
        fw.write(info)
        print(info)
        print("New file name: ", self.format_file_name(file_name))
