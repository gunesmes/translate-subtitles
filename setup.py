from setuptools import setup, find_packages

setup(
    name = "transitle",
    version = "0.0.1",
    author = "Mesut Gunes",
    author_email="gunesmes@gmail.com" ,
    description = "Translate subtitles in a folder",
    long_description= "transitle allows you to translate subtitles in a directory flawlessly with your favorite translator.",
    readme = "README.md",
    license="LICENSE.md",
    url = "https://github.com/gunesmes/subtitle_translator",
    packages=find_packages(include=('ts.*', 'transitle')),
    entry_points={
        'console_scripts': ['ts = transitle.__main__:main']
    },
    python_requires=">=3.0",
    install_requires=['googletrans']
)