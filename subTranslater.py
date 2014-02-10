# -*- coding: utf-8 -*-
import goslate
import time

# Author Name: Mesut Güneş
# Author Email: gunesmes@gmail.com
# Author Github username: gunesmes

class SubsTranslater():
    def read_file(self, fileName):
        fr = open(fileName, "r")
        lines = fr.readlines()
        fr.close()
        
        return lines
    
    def write_file(self, fileName, target_language, source_language):
        fn = self.format_file_name(fileName, target_language, source_language)   
        fw = open(fn, 'w')
    
        return fw
        
    def format_file_name(self, fileName, target_language, source_language):
        name_sep = "_" + source_language + "_to_" + target_language

        #index number of last dot
        lastDot = fileName.rfind('.')   
        
        # means that there is no dot in the file name, 
        # and file name has no file type extension 
        if lastDot == -1:               
            newFileName = fileName + str(name_sep) + '.srt'
            
        else:
            baseName = fileName[0: lastDot]
            ext = fileName[lastDot: len(fileName)]            
            newFileName = baseName + str(name_sep) + ext            
                                            
        return newFileName                                
    
    def prepare_line(self, line):
        # preparing line before sending to google translate
        # unexpected characters will be removed
        # uncompleted sentences will be unified
        
        line        = line[1:] #remove added space
        line_       = ""
        prefix      = ""
        suffix      = ""
        
        # check if the line has any characters like these "<i>", "<b>", "<u>", "</i>, "</b>
        # check if it is like "<i> ... </i>"
        try:
            if line[0] == "<" and line[2] == ">" and line[-1] == ">" and line[-4] == "<":
                line_       = line[3:-4]
                prefix      = line[0:3]
                suffix      = line[-4:]
                
            # check if it is like "<i> ... "
            elif line[0] == "<" and line[2] == ">" and line[-1] != ">" and line[-4] != "<":
                line_       = line[3:]
                prefix      = line[0:3]
            
            # check if it is like " ... </i>"
            elif line[0] != "<" and line[2] != ">" and line[-1] == ">" and line[-4] == "<":
                line_       = line[0:-4]
                suffix      = line[-4:]
              
            else:
                line_       = line
        except:
            line_       = line
            
        return (line_, prefix, suffix)
    
    
    def send_google_translator(self, prepared_sub, target_language, source_language):
        # more info about language abbreviation
        # https://developers.google.com/translate/v2/using_rest#language-params
        try:
            gs = goslate.Goslate()
        except:
            print "Wait and send again"
            time.sleep(5)
            gs = goslate.Goslate()
        
        return gs.translate(prepared_sub, target_language, source_language)
    
            
    def prepare_translated_sub(self, translated_sub, prefix, suffix, _max_length):
        translated_split_lines = {}
        lines                  = ""
        translated_lines       = {}
        temp_lines             = {}
        i                      = 0
        total_len              = 0
        max_length             = _max_length 
        
        # if the subtitle has dialogs
        if ". -" in translated_sub:
            translated_sub_tmp = translated_sub.split(". -")
            
            # separate dialogs
            translated_sub_dia = {}
            translated_sub_dia[0] = translated_sub_tmp[0] + "."
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
                            #if remaining part is shorter than max_length
                            translated_lines[i] = lines + word + suffix
                        else:
                            lines       += word + " "
                            total_len   += len(word) + 1
                        
                    else:
                        # set number of characters shown in screen by max_length
                        # if first line should have prefix, and last line should have suffix
                        # if last word left alone, it's added to the previous line
                        temp_lines[i]       = [lines, (prefix + lines)][i == 0]
                        translated_lines[i] = [temp_lines[i], (lines + word + suffix)][word == words[-1]] 
                        i                  += 1
                        lines               = ""
                        lines              += word + " "
                      
            
            else:    
                translated_lines[i] = prefix + translated_split_lines[i] + suffix

        return translated_lines

    def translate_substitle(self, fileName, target_language, source_language, translator, _max_length):
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
        fw          = self.write_file(fileName, target_language, source_language) 
        lines       = self.read_file(fileName)
        line        = str()
        
        i = 0
        for i in range(len(lines)):
            #print lines[i]
            
            # print non-translatable lines 
            if lines[i].rstrip().isdigit() and "-->" in lines[i+1] or "-->" in lines[i]:
                fw.write(lines[i])
                print lines[i].strip()
                continue
            
            # concatenate lines until empty line:
            while not lines[i].rstrip()=="":
                line += " " + lines[i].rstrip()
                break
            
            if lines[i].rstrip()=="": 
                # prepare line before sending translator
                serilized_sub   = self.prepare_line(line)
                prepared_sub    = serilized_sub[0]
                prefix          = serilized_sub[1]
                suffix          = serilized_sub[2]
                
                if translator.lower() == "google":
                    # send prepared subtitle to google translate
                    translated_sub = self.send_google_translator(prepared_sub, target_language, source_language)
                 
                # prepare sub before writing new subtitle file
                prepared_lines = self.prepare_translated_sub(translated_sub, prefix, suffix, _max_length)
                for i in range(len(prepared_lines)):
                    print prepared_lines[i]
                    fw.write(str("%s\n" %prepared_lines[i]))
                    
                fw.write("\n")
                print ""
                line = ""
                       
        print "New file name: ", self.format_file_name(fileName, target_language, source_language)


