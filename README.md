Translate Subtitles - transitle
===================
translate_subtitles allows you to translate subtitles in a directory flawlessly with your favorite translator.
Translate bunch of subtitles from original language to desired language. This gives you a machine translated subtitle.

`pip install transitle`

<!---
![Subtitle Demo Gif](img/tty.gif)
--->

# To run the translater
* install the `transitle` via pip
    `pip install transitle`
* you must have a valid subtitle in .srt format
* You can use Google translator or yandex
* For yandex you must have Yandex Translater API key. You can get it from here: http://api.yandex.com/key/keyslist.xml

## Run as a CLI tooling

```shell
➜  ~ pip install transitle
➜  ~ ts ~/Downloads/subtitles google en tr

 - - - - - - - - Translating: sample.srt - - - - - - - -
1
00:00:09,750 --> 00:00:10,666
<i>São Paulo,</i>

2
00:00:10,750 --> 00:00:13,166
<i>neredeyse 13 milyon kişi.</i>
```

## Use as a library
```shell
# translate subtitles in a path
>>> from transitle import ts
>>> ts('/Users/mesutgunes/Downloads/subtitles', 'google', 'en', 'tr')

 - - - - - - - - Translating: sample.srt - - - - - - - -
1
00:00:09,750 --> 00:00:10,666
<i>São Paulo,</i>

2
00:00:10,750 --> 00:00:13,166
<i>neredeyse 13 milyon kişi.</i>

3
00:00:13,250 --> 00:00:16,583
<i>Hikayemin bu kısmı burada başladı.
sonbaharda.</i>

# translate a subtitle
>>> from translate_subtitles import TranslateSubtitle
>>> tr = TranslateSubtitle()
>>> tr.subtitle_translator('/Users/mesutgunes/Downloads/subtitles/sample.srt', 'google', 'en', 'tr')

 - - - - - - - - Translating: sample.srt - - - - - - - -
1
00:00:09,750 --> 00:00:10,666
<i>São Paulo,</i>

2
00:00:10,750 --> 00:00:13,166
<i>neredeyse 13 milyon kişi.</i>
```

# Local Development
Make sure you have Python 2.7 or above installed
Check Python:
```shell
python --version
```

Clone the project:
```shell
>>> git clone https://github.com/gunesmes/subtitle_translator.git

# edit code and install it
>>> pip3 install .  

# use it as normal
>>> ts('/Users/mesutgunes/Downloads/subtitles', 'google', 'en', 'tr') 
```

- Don't wory about source language, translater can understand it. (not released)
- Check language abbreviation: https://developers.google.com/translate/v2/using_rest#language-params
- The .srt files in the given directory are to be translated to target language 
