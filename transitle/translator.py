from datetime import datetime
import os
import pdb
from transitle.ts import TranslateSubtitle

out = '/out/'

def ts(file_dir, translator, source_lang, target_lang):
    start_time = datetime.now()
    
    # set absolute paths
    abs_path = os.path.abspath(file_dir)
    translation_path = abs_path + out

    # change directory
    os.chdir(abs_path)

    ts = TranslateSubtitle(
        abs_path=abs_path, 
        out=translation_path, 
        translator=translator,
        source_lang=source_lang,
        target_lang=target_lang
        )

    # get the .srt files from the dir
    files = os.listdir(abs_path)
    str_files = list()
    for item in files:
        if item.rfind(".srt") != -1:
            str_files.append(item)
            continue

    for file in str_files:
        print(f"\n - - - - - - - - Translating: {file} - - - - - - - - ")

        """
        this function translate a subtitle file from original language to desired  language
        
        fileName        : names of subtitles 
        target_lang     : language you want to translate to
        source_lang     : the language of the subtitle
        translator      : Google (later Yandex, Microsoft)
        """

        ts.subtitle_translator(file)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
