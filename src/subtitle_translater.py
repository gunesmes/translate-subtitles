# -*- coding: utf-8 -*-
# Author Name: Mesut Güneş
# Author Email: gunesmes@gmail.com
# Author Github username: gunesmes

import pdb
import goslate
import time, requests, codecs, sys, urllib, random, os

# get yandex translate key from: https://tech.yandex.com/keys/?service=trnsl
YANDEX_API_KEY = "trnsl.1.1.20160603T091015Z.87ae2d901d0e30b5.c07fcad534693b23c6b5151e4284d79702efd762"
GOOGLE_TRANSLATION_LIMIT = 500

class SubsTranslater:

    @staticmethod
    def read_file(file_name):
        fr = codecs.open(file_name, "r", encoding='utf-8-sig')
        lines = fr.readlines()
        fr.close()

        return lines

    @staticmethod
    def read_file_as_list(file_name):
        fr = codecs.open(file_name, "r", encoding='utf-8-sig')
        lines = fr.read()
        fr.close()

        return lines.split("\r\n\r\n")

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
    def prepare_line(line):
        # preparing line before sending to google translate
        # unexpected characters will be removed
        # uncompleted sentences will be unified

        line = line[1:]  # remove added space
        line_ = ""
        prefix = ""
        suffix = ""

        # check if the line has any characters like these "<i>", "<b>", "<u>", "</i>, "</b>
        # check if it is like "<i> ... </i>"
        try:
            if line[0] == "<" and line[2] == ">" and line[-1] == ">" and line[-4] == "<":
                line_ = line[3:-4]
                prefix = line[0:3]
                suffix = line[-4:]

            # check if it is like "<i> ... "
            elif line[0] == "<" and line[2] == ">" and line[-1] != ">" and line[-4] != "<":
                line_ = line[3:]
                prefix = line[0:3]

            # check if it is like " ... </i>"
            elif line[0] != "<" and line[2] != ">" and line[-1] == ">" and line[-4] == "<":
                line_ = line[0:-4]
                suffix = line[-4:]

            else:
                line_ = line
        except:
            line_ = line

        return line_, prefix, suffix

    @staticmethod
    def send_google_translator(prepared_sub, source_language, target_language):
        # Using Google API is not free so we can send sentences via browser for this Goslate module 
        # is written by ZHUO Qiang. For more information http://pythonhosted.org/goslate/#module-goslate
        # More info about language abbreviation
        # https://developers.google.com/translate/v2/using_rest#language-params
        try:
            gs = goslate.Goslate()
        except:
            print("Wait and send again")
            time.sleep(5)
            gs = goslate.Goslate()

        return gs.translate(prepared_sub, target_language, source_language)

    @staticmethod
    def send_yandex_translator(prepared_sub, source_language, target_language):
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

    @staticmethod
    def prepare_translated_sub(translated_sub, prefix, suffix, _max_length):
        translated_split_lines = {}
        lines = ""
        translated_lines = {}
        temp_lines = {}
        i = 0
        total_len = 0
        max_length = _max_length

        # if the subtitle has dialogs
        if ". -" in translated_sub:
            translated_sub_tmp = translated_sub.split(". -")

            # separate dialogs
            translated_sub_dia = {0: translated_sub_tmp[0] + "."}
            for i in range(1, len(translated_sub_tmp)):
                translated_sub_dia[i] = "-" + translated_sub_tmp[i]

            translated_split_lines = translated_sub_dia

        else:
            translated_split_lines[0] = translated_sub

        for i in range(len(translated_split_lines)):
            if len(translated_split_lines[i]) > max_length:
                words = translated_split_lines[i].split(" ")

                for word in words:
                    if len(lines + word) <= max_length:
                        if word == words[-1]:
                            # if remaining part is shorter than max_length
                            translated_lines[i] = lines + word + suffix
                        else:
                            lines += word + " "
                            total_len += len(word) + 1

                    else:
                        # set number of characters shown in screen by max_length
                        # if first line should have prefix, and last line should have suffix
                        # if last word left alone, it's added to the previous line
                        temp_lines[i] = [lines, (prefix + lines)][i == 0]
                        translated_lines[i] = [temp_lines[i], (lines + word + suffix)][word == words[-1]]
                        i += 1
                        lines = ""
                        lines += word + " "


            else:
                translated_lines[i] = prefix + translated_split_lines[i] + suffix

        return translated_lines

    def translate_subtitle(self, file_name, source_language, target_language, translator, _max_length):
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
        fw = self.write_file(file_name, target_language, source_language)
        lines = self.read_file_as_list(file_name)
        line = str()

        i = 0
        for i in range(len(lines)):
            # print non-translatable lines 
            if lines[i].rstrip().isdigit() and "-->" in lines[i + 1] or "-->" in lines[i]:
                fw.write(lines[i])
                print(lines[i].strip())
                continue

            # concatenate lines until empty line:
            while not lines[i].rstrip() == "":
                line += " " + lines[i].rstrip()
                break

            if lines[i].rstrip() == "":
                # prepare line before sending translator
                serialized_sub = self.prepare_line(line)
                prepared_sub = serialized_sub[0]
                prefix = serialized_sub[1]
                suffix = serialized_sub[2]

                time.sleep(random.random())  # sleep some random 0 to 1 second
                if translator.lower() == "google":
                    # send prepared subtitle to Google translator
                    translated_sub = self.send_google_translator(prepared_sub, source_language, target_language)

                elif translator.lower() == "yandex":
                    # send prepared subtitle to Yandex translator
                    translated_sub = self.send_yandex_translator(prepared_sub, source_language, target_language)

                # prepare sub before writing new subtitle file
                prepared_lines = self.prepare_translated_sub(translated_sub, prefix, suffix, _max_length)
                for i in range(len(prepared_lines)):
                    print(prepared_lines[i])
                    fw.write(str("%s\n" % prepared_lines[i]))

                fw.write("\n")
                print("")
                line = ""

        # Print information about the subtitle
        info = "Translated by subtitle_translator via %s translator \nwritten by Mesut Gunes: https://github.com/gunesmes/subtitle_translator\n" % translator.upper()
        fw.write(info)
        print(info)
        print("New file name: ", self.format_file_name(file_name, target_language, source_language))


    def translate_subtitle_raw(self, file_name, source_language, target_language, translator_tool, _max_length):
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
        fw = self.write_file(file_name, target_language, source_language)
        content_list = self.read_file_as_list(file_name)
        durations = []
        contents = []
        text_translatable = ''
        # from googletrans import Translator
        from googletranslatepy import Translator
        translator = Translator(source=source_language, target=target_language)

        for content in content_list:
            # print non-translatable lines
            lines = content.split("\r\n")
            time_info = ''
            text_info = ''
            for i in range(len(lines)):
                if lines[i].rstrip().isdigit() and "-->" in lines[i + 1] or "-->" in lines[i]:
                    time_info += lines[i] + "\r\n"
                    continue
                else:
                    text_info += lines[i] + "\n" 
                
            if len(text_info) + len(text_translatable) < GOOGLE_TRANSLATION_LIMIT:                
                durations.append(time_info)
                text_translatable += text_info + "\n\r"
            else:
                try:  
                    translated_sub = translator.translate(text_translatable)
                    temp_translated = translated_sub.split("\n\r")
                    temp_translated[-1] = temp_translated[-1] + "\n"
                    contents += temp_translated
                except TypeError as err:
                    translated_sub = 'err'
                    print(err)
                    
                text_translatable = text_info
                time.sleep(5)
                
        for d, c in zip(durations, contents):
            # pdb.set_trace() 
            fw.write(d)
            fw.write(c + "\n")
            print(d + c)

        # if lines[i].rstrip() == "":
        #     # prepare line before sending translator
        #     serialized_sub = self.prepare_line(line)
        #     prepared_sub = serialized_sub[0]

        #     time.sleep(random.random())  # sleep some random 0 to 1 second
        #     if translator.lower() == "google":
        #         # send prepared subtitle to Google translator
        #         translated_sub = self.send_google_translator(prepared_sub, source_language, target_language)

        #     elif translator.lower() == "yandex":
        #         # send prepared subtitle to Yandex translator
        #         translated_sub = self.send_yandex_translator(prepared_sub, source_language, target_language)

        #     # prepare sub before writing new subtitle file
        #     prepared_lines = self.prepare_translated_sub(translated_sub, prefix, suffix, _max_length)
        #     for i in range(len(prepared_lines)):
        #         print(prepared_lines[i])
        #         fw.write(str("%s\n" % prepared_lines[i]))

        #         fw.write("\n")
        #         print("")
        #         line = ""

        # Print information about the subtitle
        info = "Translated by subtitle_translator via %s translator \nwritten by Mesut Gunes: https://github.com/gunesmes/subtitle_translator\n" % translator_tool
        fw.write(info)
        print(info)
        print("New file name: ", self.format_file_name(file_name, target_language, source_language))
