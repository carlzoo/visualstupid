#!/usr/bin/python
import os

def check_compilers():
	compilers={'gcc':'/usr/bin/gcc',
				'g++': '/usr/bin/g++',
			   'clang':'/usr/bin/cc',
			   'java': '/usr/bin/javac',
				'perl':'/usr/bin/perl',
				'python':'/usr/bin/python',
				'racket': '/usr/bin/racket',
				'ruby':'/usr/bin/ruby'}

	print "Checking for compilers available..."
	
	for compiler in compilers:
		if which(compilers[compiler]):
			print compiler + ' found'
		else:
			print compiler + ' not found!'

#https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python	
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return True

    return False
