#!/usr/bin/python

import sys
import os
import platform
import fnmatch

from picture import *
from checks import check_compilers

#https://stackoverflow.com/questions/5508110/why-is-this-program-erroneously-rejected-by-three-c-compilers/5509143

def main():
	helpmessage='''
	python visualstupid.py [option] <input file>
	options:
	-f <image>				Compile individual image
	-r <directory>			Compile all images in directory (recursively)
	-m <makefile image>		Execute makefile (not supported at the moment)
	'''

	if len(sys.argv) < 3:
		sys.exit(helpmessage)

	check_compilers()
	
	option=sys.argv[1]
	if option == '-f':
		single_file_mode()
	elif option == '-r':
		filelist=[]
		for root, dirnames, filenames in os.walk(sys.argv[2]):
			for filename in filenames:
				if filename.endswith(('.jpg', '.jpeg', '.gif', '.png','.tiff')):
					filelist.append(os.path.join(root,filename))
		multiple_files_mode(filelist)
	else:
		sys.exit('invalid option')	

def single_file_mode():
	compile_picture(Picture(sys.argv[2],'eng'))
	return

def multiple_files_mode(filelist):
	#sort the list to put header files first
	headerlist=[]
	notheaderlist=[]
	for f in filelist:
		p=Picture(f,'eng')
		p.guess_language()
		if p.isHeaderFile:
			headerlist.append(f)
		else:
			notheaderlist.append(f)
	filelist=headerlist + notheaderlist

	#compile all files
	for f in filelist:
		compile_picture(Picture(f,'eng'))
	return

def compile_picture(p):
	delimiter='/'
	#determine the operating system
	operatingSystem=platform.system()
	if operatingSystem == 'Windows':
		delimiter='\\'

	p.guess_language()	
	p.imagetotext()
	if p.isHeaderFile:
		return

	cmd='ls'
	if p.proglang == 'c':
		arr=p.outputname.split(delimiter)
		fname=arr[len(arr)-1]
		fname=fname[:-2]
		cmd='gcc ' + p.outputname + ' -o ' + fname
	elif p.proglang == 'c++':
		arr=p.outputname.split(delimiter)
		fname=arr[len(arr)-1]
		fname=fname[:-4]
		cmd='g++ ' + p.outputname + ' -o ' + fname
	elif p.proglang == 'java':
		cmd='javac ' + p.outputname
	elif p.proglang == 'python':
		cmd='python2 ' + p.outputname
	elif p.proglang == 'racket':
		cmd='raco make ' + p.outputname
	elif p.proglang == 'ruby':
		cmd='ruby ' + p.outputname
	elif p.proglang == 'perl':
		cmd = 'perl ' + p.outputname
	else:
		sys.exit('invalid programming language: ' + p.proglang)

	print '\nrunning compilation'
	os.system(cmd)

if __name__ == "__main__":
	main()
			
