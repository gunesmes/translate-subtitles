import codecs
import os
from setuptools import setup, find_packages

pwd = os.path.dirname(os.path.abspath(__file__))

# Get the long description
with codecs.open(os.path.join(pwd, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n{}'.format(f.read())
    os.system("pwd")
    os.system("ls -lrt")

# # Get change log
# with codecs.open(os.path.join(pwd, 'CHANGELOG'), encoding='utf-8') as f:
#     changelog = f.read()
#     long_description += '\n\n{}'.format(changelog)


setup(
    name = "transitle",
    version = "1.0.1",
    author = "Mesut Gunes",
    author_email = "gunesmes@gmail.com" ,
    description = "Translate subtitles in a folder flawlessly",
    long_description = '''translate_subtitles allows you to translate subtitles in a directory flawlessly with your favorite translator. 
        Translate bunch of subtitles from original language to desired language. This gives you a machine translated subtitle.
    ''',
    license = "LICENSE.md",
    url = "https://github.com/gunesmes/subtitle_translator",
    packages = find_packages(include=('ts.*', 'transitle')),
    entry_points = {
        'console_scripts': ['ts = transitle.__main__:main']
    },
    python_requires = ">=3.0",
    install_requires = ['googletranslate_python', 'requests']
)
