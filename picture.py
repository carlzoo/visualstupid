#!/usr/bin/python

from PIL import Image
import pyocr
import pyocr.builders
import codecs

import os
import platform

class Picture:
	def __init__(self,filepath='.',lang='eng'):
		self.filepath=filepath
		self.ocrlang=lang
		self.builder=pyocr.builders.TextBuilder()
		self.proglang='unknown'
		self.outputname=''
		self.isHeaderFile=False

	#guess the language based on the file name
	def guess_language(self):
		delimiter='/'
		#determine the operating system
		operatingSystem=platform.system()
		if operatingSystem == 'Windows':
			delimiter='\\'
	
		fp=self.filepath.split(delimiter)
		length=len(fp)
		fname=fp[length-1].lower()
		if '.java.' in fname:
			self.proglang='java'
		elif '.cpp.' in fname:
			self.proglang='c++'
		elif '.c.' in fname:
			self.proglang='c'
		elif '.py.' in fname:
			self.proglang = 'python'
		elif '.rkt.' in fname:
			self.proglang = 'racket'
		elif '.rb.' in fname:
			self.proglang = 'ruby'
		elif '.pl.' in fname:
			self.proglang = 'perl'
		elif '.h.' in fname:
			self.proglang='c'
			self.isHeaderFile=True
		else:
			raise "unknown programming language"

	def imagetotext(self):
		tool = pyocr.get_available_tools()[0]
		builder=pyocr.builders.TextBuilder()		

		txt = tool.image_to_string(
			Image.open(self.filepath),
			lang=self.ocrlang,
			builder=pyocr.builders.TextBuilder()
		)
		
		#strip picture file extension
		self.outputname=self.filepath.replace('.png','').replace('.jpg','').replace('.gif','').replace('.tiff','')
		self.outputname=self.outputname.replace('.PNG','').replace('.JPG','').replace('.GIF','').replace('.TIFF','')

		#write to output file
		with codecs.open(self.outputname, 'w', encoding='utf-8') as file_descriptor:
			builder.write_file(file_descriptor, txt)
