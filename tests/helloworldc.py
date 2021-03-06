from PIL import Image
import sys
import os

import pyocr
import pyocr.builders

import codecs

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.

builder = pyocr.builders.TextBuilder()

txt=tool.image_to_string(
	Image.open('images/helloworld.c.png'),
	lang='eng',
	builder=pyocr.builders.TextBuilder()
)

print txt

with codecs.open("helloworld.c", 'w', encoding='utf-8') as file_descriptor:
    builder.write_file(file_descriptor, txt)

os.system('gcc helloworld.c -o helloworld')
