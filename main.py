import socket
import socks
import random
import dns.resolver 
import threading
import thread
import urllib2
import urllib
import twitter
import time
import threading
import re
import commands
from bs4 import BeautifulSoup
from commands import *

global tweeted
tweeted = 0
global used
used = 0

def floodCounter():
	while 1:
		 #flood = {}
		 global tweeted
		 tweeted = 0
		 time.sleep(120)
		 
def floodFilter():
	while 1:
		 #flood = {}
		 global used
		 used = 0
		 time.sleep(3) 

#Setup spam filters
thread.start_new_thread(floodCounter,())
thread.start_new_thread(floodFilter,())

def Net():
	#Bot Configuration
	nick = 'Iris_'
	host = "irc.tm"
	channel = "#mootsinsuits"
	packets = ["NICK %s" % nick + "\r\n", "USER " + nick + " " + nick + " " + nick + " :" + nick + "\r\n", "JOIN %s" % channel + "\r\n"]
	#Connect to IRC Server
	s = socket.socket()
	s.connect((host, 6667));
	
	#Send packs
	for packet in packets:
		s.send(packet);
	cmds = {}
	while True:
		data = s.recv(1024);
		data = data.strip();
		print data
		if data.find(" 376 ") != -1:
			send(s, "JOIN %s\r\n" % (channel))
			
		if data.startswith("PING "):
			hash_key = data.split("PING :");
			send(s, "PONG %s\r\n" % (hash_key[1]))
		
		if "PRIVMSG " in data:
			channel = data.split("PRIVMSG ")
			channel = channel[1].split(" :")
			channel = channel[0].strip()
			print channel
			sData = data.split(" PRIVMSG "+channel+" :")[1].strip()
			
			if sData.startswith(".j "):
				chan = data.split(".j ")
				chan = chan[1].strip()
				send(s, "JOIN %s\r\n" % (chan))
				
			if sData.startswith(".skype "):
				name = data.split(".skype ")[1].strip()
				print name
				p = SkypeResolver()
				if(name == "blacklisted-username"): #Add your blacklists here? Not really needed
					print "no"
				else:
					q = p.ResolveIP(name)
					print q
					#send(s, "PRIVMSG %s :API broken till further notice\r\n" % (channel))
					send(s, "PRIVMSG %s :ip - %s\r\n" % (channel, q))
			
			if sData.startswith(".addCommand '"):
				name = user(data)
				yn = whois(s, name)
				if yn == True:
					if data.startswith(":Luga!"):
						args = data.split(".addCommand ")[1].strip()
						args = args.split(":", 1)
						cmds[args[0].replace("'", "")] = args[1].replace("'", "")
						send(s, "PRIVMSG %s :Command %s added\r\n" % (channel, args[0]))
				else:
					send('PRIVMSG %s :How about you go suck on a big fat chode\r\n' % (channel))
				
			if cmds.has_key(sData.strip()):
				eval(cmds[sData.strip()])#(s,channel)
				
			if sData.startswith(".list"):
				send(s, "PRIVMSG %s :Commands in list %s\r\n" % (channel, str(cmds)))
				
			if sData.startswith('.ip '):
				try:
					site = data.split('.ip')[1].strip()
					getIp(s, site, channel)				
				except(ValueError, socket.gaierror):	
					send('PRIVMSG %s :Incorrect usage of command\r\n' % (channel))
			
			if sData.startswith('.ipv6 '):
				try:
					site = data.split('.ipv6 ')[1].strip()
					site = site.strip()
					getIpv6(s, site, channel)
				except(ValueError, socket.gaierror, dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):	
					send(s, 'PRIVMSG %s :Incorrect usage of command or no ipv6 found\r\n' % (channel))  
					pass
				
			if sData.startswith("!ryan"):
				ryan(s, channel)
				
			if sData.startswith(".access "):
				name = user(data)
				yn = whois(s, name)
				if yn == True:
					if data.startswith(":Luga!") or data.startswith(":niggerbread!"):
						name = data.split('.access ')[1]
						access(s, name, channel, data)
				else:
					send(s, 'PRIVMSG %s :How about you go suck on a big fat chode\r\n' %s (channel))
			
			if sData.startswith("!tweet "):
				name = user(data)
				global tweeted
				if tweeted == 1:
					send(s, 'PRIVMSG %s :Someone has already tweeted within the 2 minute limit\r\n' % (name))
				else:
					message = data.split('!tweet ')[1]
					sendTweet(s, name, message, channel)
					tweeted = 1
					
			if sData.startswith("!deltweet "):
				name = user(data)
				message = data.split('!deltweet ')[1]
				deleteTweet(s, name, message, channel)
				
			if sData.startswith("!retweet "):
				name = user(data)
				global tweeted
				if tweeted == 1:
					send(s, 'PRIVMSG %s :Someone has already tweeted within the 2 minute limit\r\n' % (name))
				else:
					message = data.split('!retweet ')[1]
					sendReTweet(s, name, message, channel)
					tweeted = 1
					
			if sData.startswith("!geoip "):
				ip = data.split('!geoip ')[1]
				geoIP(s, ip, channel)	
				
			if sData.startswith("!news"):
				news(s, channel)
				
			if (data.find("!whois ") != -1):
				name = user(data)
				whois(s, name)
				
			if sData.startswith(".ping"):
				if sData.startswith(".ping "):
					try:
						site = sData.split(" ")[1]
						t = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",site)
						if (t):
							pingIp(s, site, channel)
						else:
							pingSite(s, site, channel)
					except Exception as e:
						send(s, 'PRIVMSG %s :Ip/site is probably down\r\n' % (channel))
						send(s,'PRIVMSG %s :%s\r\n' % (channel, str(e)))
						pass
				else:
					send(s, 'PRIVMSG %s :Pong\r\n' % (channel))
	
			if sData.startswith(".help"):
				name = user(data)
				help(s, name)
			
			if sData.startswith("!random"):
				r = random.randrange(0, 10)
				send(s, 'PRIVMSG %s :%s\r\n' % (channel, r))
				
			if(sData.startswith(".reload")):
				#reload(commands)
				#from commands import *
				#del commands
				if 'commands' in sys.modules:  
					del(sys.modules["commands"]) 
					import commands
					send(s, 'PRIVMSG %s :Reloaded command module\r\n' % (channel))
				
			if(sData.startswith(".cf ")):
				site = sData.split('.cf ')[1]
				cloudFlareResolver(s, site, channel)
				
			if sData.startswith("http://") or sData.startswith("https://"):
				try:
					#proxies = {'http': '127.0.0.1:8118'}
					site = sData.split("://")[1]
					site = "http://"+site.strip()
					page = urllib.urlopen(site)
					soup = BeautifulSoup(page)
					title = soup.title.string
					title = str(title).strip()
					send(s, 'PRIVMSG %s :%s - %s\r\n' % (channel, site, title))
				except Exception as e:
					send(s, 'PRIVMSG ' + channel + ' :%s\r\n' % str(e))  
					pass       
				
Net()	
