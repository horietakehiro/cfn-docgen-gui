import sys
from cx_Freeze import setup, Executable

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable(
        'main.py', base=base,
        shortcutName="cfn-docgen-gui",
        shortcutDir="DesktopFolder",
    )
]

setup(
    name = 'cfn-docgen-gui',
    version='0.2.0',
    description='GUI app for cfn-docgen',
    executables=executables,
    author = 'Takehiro Horie',
    author_email = 'horie.takehiro@outlook.jp',
    license = 'MIT License',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/horietakehiro/cfn-docgen-gui',

)