from datetime import datetime
import os

from transitle.ts import TranslateSubtitle


def ts(file_dir, translator, source_lang, target_lang):
    start_time = datetime.now()
    
    # set directory
    os.chdir(file_dir)
    path = os.listdir(file_dir)

    s = TranslateSubtitle()

    # get the .srt files from the dir
    files = list()
    for item in path:
        if item.rfind(".srt") != -1:
            files.append(item)
            continue

    for file in files:
        print(f"\n - - - - - - - - Translating: {file} - - - - - - - - ")
        subFile = os.path.dirname(os.path.abspath(file)) + "/" + file

        """
        this function translate a subtitle file from original language to desired  language
        
        fileName        : names of subtitles 
        target_language : language you want to translate to
        source_language : the language of the subtitle
        translator      : Google (later Yandex, Microsoft)
        """

        s.subtitle_translator(subFile, translator, source_lang, target_lang)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))