#!/usr/bin/python
import subprocess
import os
import getpass

password = ''
filename = ''
path = ''
def createFile():
	createDiary="touch %s" % (filename)
	os.system(createDiary)
	print 'create new diary %s' % (filename)
	encrypt(filename)


def menu():
	operate={'w':'writeDiary', 'r':'readDiary', 'c':'changePassword'}
	print 'write (w)	read (r)	changepassword(c)'
	work = raw_input('Enter your choice: ')
	if work == 'r':
		readDiary()
	elif work == 'w':
		writeDiary()
	elif work == 'c':
		changePassword()
	else:
		print 'illigel command.'

def writeDiary():
	global path
	global filename
	tpfile = path + r'/.tpfile'
	editFile = 'vi %s' % (tpfile) 
	os.system(editFile)
	if os.path.exists(filename):
		originDiary=decrypt(filename)
	else:
		os.system('touch %s/.temfile' % (path))
		originDiary = 'temfile'
	if os.path.exists(tpfile):
		open(originDiary, 'a').writelines(open(tpfile, 'r').readlines())	
		os.system('rm %s*' % (tpfile))
	encrypt(originDiary)
	os.system('rm %s*' % (originDiary))
	
	
def readDiary():
	global filename
	originDiary = decrypt(filename)
	os.system('tail %s | less ' % (originDiary))
	os.system('rm %s' % (originDiary))

def main():
	print 'Please Enter your password: '
	global password 
	password = getpass.getpass()
	print password
	name = subprocess.Popen(['whoami'], stdout=subprocess.PIPE)
	myname = name.stdout.read().strip('\n')
	global path 
	path = '/home/' + myname + '/diary'
	global filename
	filename = path + '/' + myname + 'Diary'
	decrypt(filename)
	menu()

def encrypt(originDiary):
	global filename
	global password
	
	encryptionDiary = 'openssl enc -des -a -in %s -out %s -k %s' % (originDiary, filename, password)
	os.system(encryptionDiary)
	
def decrypt(filename):
	global path
	global password
	tempfile = path + r'/.tempfile'
	if os.system('openssl enc -des -d -a -in %s -out %s -k %s 1>/dev/null 2>&1' % (filename, tempfile, password)):
		print 'bad decrypt'
		exit(0)
	else:
		return tempfile

def changePassword():
	global password
	global filename
	originDiary = decrypt(filename)
	password = getpass.getpass('Please enter your new password: ')
	encrypt(originDiary)
	os.system('rm %s' % (originDiary))

if __name__ == '__main__':
	main()
	
