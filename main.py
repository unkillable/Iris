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
import os
import sys
from commands import *
from auto_kick import akick_list
from todo import todo_list
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
	nick = 'Iris'
	host = "irc.niggerbread.me"
	channel = "#iffi"
	packets = ["NICK %s" % nick + "\r\n", "USER " + nick + " " + nick + " " + nick + " :" + nick + "\r\n", "JOIN %s" % channel + "\r\n"]
	#Connect to IRC Server
	s = socket.socket()
	s.connect((host, 6667));
	
	#Send packs
	for packet in packets:
		s.send(packet);
	cmds = {}
	topic = ""
	while True:
		data = s.recv(1024)
		data = data.strip();
		print data
		if data.find(" 376 ") != -1:
			send(s, "JOIN %s\r\n" % (channel))
			send(s, "PRIVMSG nickserv identify isis4days\r\n")
			
		if data.startswith("PING "):
			hash_key = data.split("PING :");
			send(s, "PONG %s\r\n" % (hash_key[1]))
		if data == "":
			print "Ping timeout occured. Restarting"
			s.close()
			os.system("python main.py")
		if " has changed the topic to:" in data:
			#file = open("current_topic", "w+")
			#file.write(data.split(" has changed the topic to:")[1].strip())
			#file.close()
			topic = data.split(" has changed the topic to:")[1].strip()
		if "Iris " + channel + " :" in data:
			try:
				print "Found topic"
				global topic
				#file = open("current_topic", "w+")
				#file.write(data.split(" 332 Iris " + channel + " :")[1].strip())
				#file.close()
				topic = data.split(" 332 Iris " + channel + " :")[1].split("\n")[0].strip()
			except Exception as e:
				pass
		if "PRIVMSG " in data:
			channel = data.split("PRIVMSG ")
			channel = channel[1].split(" :")
			channel = channel[0].strip()
			print channel
			sData = data.split(" PRIVMSG "+channel+" :")[1].strip()
			for user in akick_list:
				if data.startswith(":"+user+"!"):
					send(s, "KICK %s %s\r\n" % (channel, user))
			if sData.startswith(".j "):
				chan = data.split(".j ")
				chan = chan[1].strip()
				send(s, "JOIN %s\r\n" % (chan))
			
			if sData.startswith(".p "):
				chan = data.split(".p ")
				chan = chan[1].strip()
				send(s, "PART %s\r\n" % (chan))			
			if sData.startswith(".quit"):
				send(s, "QUIT \r\n")
				s.close()
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
					send(s, 'PRIVMSG %s :How about you go suck on a big fat chode\r\n' % (channel))
				
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
					send(s, 'PRIVMSG %s :How about you go suck on a big fat chode\r\n' % (channel))
			
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
				try:
					ip = data.split('!geoip ')[1]
					geoIP(s, ip, channel)		
				except Exception as e:
					pass
				
			if sData.startswith("!geo "):
				try:
					ip = data.split('!geo ')[1]
					geoIP(s, ip, channel)		
				except Exception as e:
					pass
				
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
					title = str(title).strip().encode('utf-8')
					send(s, 'PRIVMSG %s :%s - %s\r\n' % (channel, site, title))
				except Exception as e:
					send(s, 'PRIVMSG ' + channel + ' :%s\r\n' % str(e))  
					pass
			if sData.startswith("!rotate"):
				name = user(data)
				yn = whois(s, name)
				if yn == True:
					if data.startswith(":Luga!") or data.startswith(":niggerbread!"):
						send(s, "PRIVMSG %s Rotating tor nodes\r\n" % (channel))
						send(s, "QUIT\r\n")
						s.close()
						os.system("sudo python rotate.py")
						time.sleep(5)
						os.system("sudo torify python main.py")
			if sData.startswith("!reddit"):
					reddit(s, channel)
			if sData.startswith("!subreddit "):
				try:
					board = sData.split("!subreddit ")[1].strip()
					reddit(s, channel, board)
				except Exception as e:
					send(s, "PRIVMSG %s: Please provide a valid sub-reddit\r\n" % (channel))
			
			if sData.startswith("!nextpost"):
				reddit_next(s, channel)
				
			if sData.startswith('.date'):
				send(s, "PRIVMSG %s :%s\r\n" % (channel, str(time.strftime("%m/%d/%Y"))))

			if sData.startswith('.quoteadd'):
				try:
					quote = sData.replace('.quoteadd ', '')
					theuser, quote= quote.split(" ", 1)[0], quote.split(" ", 1)[1]
					quoteAdd(s, channel, theuser, quote)
				except:
					pass
			if sData.startswith('.newestquote'):
				newestquote(s, channel)

			if sData.startswith('.quotedel'):
				if data.startswith(":Luga!") or data.startswith(":niggerbread!"):
					try:
						quote = sData.replace('.quotedel ', '')
						theuser, quote= quote.split(" ", 1)[0], quote.split(" ", 1)[1]
						quotedel(s, channel, theuser, quote)
					except:
						pass
				else:
					send(s, "PRIVMSG %s : Suck a fat one m8\r\n" % (channel))

			if sData.startswith('.quoterand'):
				quoterand(s, channel)

			if sData.startswith('.quotes'):
				if sData.startswith('.quotes '):
					theuser = data.split('.quotes ')[1].strip()
					quotes(s, channel, theuser)
				else:
					listquotes(s, channel)
			if sData.startswith('.topic '):
				thetopic = data.split('.topic ')[1].strip()
				topicadd(s, channel, thetopic)
			if sData.startswith('.topic'):
				topic(s, channel)
			if sData.startswith('.topicappend '):
				mytopic = data.split('.topicappend ')[1].strip()
				topicappend(s, channel, mytopic)

			if sData.startswith('.urbandic'):
				word = sData.split(".urbandic ")[1].strip()
				urbandic(s, channel, word)

			if sData.startswith('!news'):
				news(s, channel)
			if sData.startswith('!google '):
				request = sData.split("!google ")[1].strip()
				google(s, channel, request)
					#				except Exception as e:
					#send(s, "PRIVMSG %s :Please provide a valid search term\r\n" % (channel))
					#pass
			if sData.startswith('!4chan '):
				try:
					board = sData.split("!4chan ")[1].strip()
					print board
					fourchan(s, channel, board)
				except Exception as e:
					print e
					send(s, "PRIVMSG %s :Please provide a valid board name\r\n" % (channel))
			if sData.startswith('!4channext'):
				try:
					fourchannext(s, channel)
				except Exception as e:
					send(s, "PRIVMSG %s :Something went wrong cycling posts\r\n" % (channel))
			if sData.startswith('!notify '):
				pass
			if sData.startswith('.akick'):
				try:
					arg = sData.split('.akick ')[1]
					if arg == 'list':
						send(s, "PRIVMSG %s :Auto-kick list: %s \r\n" % (channel, str(akick_list)))
					if arg.startswith('add'):
						arg = arg.split('add ')[1].strip()
						akick_list.append(arg.strip())
						file = open("auto_kick.py", "w+")
						file.write("akick_list = " + str(akick_list))
						file.close()
						send(s, "PRIVMSG %s :%s added to auto-kick list\r\n" % (channel, arg))
					if arg.startswith('del'):
						arg = arg.split('del ')[1].strip()
						akick_list.remove(arg.strip())
						file = open("auto_kick.py", "w+")
						file.write("akick_list = " + str(akick_list))
						file.close()
						send(s, "PRIVMSG %s :%s deleted from auto-kick list\r\n" % (channel, arg))
				except Exception as e:
					send(s, "PRIVMSG %s :Please provide a valid name to add to the auto-kick list\r\n" % (channel))
				#perhaps implement notify command
			if sData.startswith('!topic '):
				try:
					top = sData.split('!topic ')[1].strip()
					send(s, "TOPIC %s :%s\r\n" % (channel, top))
					topic = top
				except Exception as e:
					print e
					send(s, "PRIVMSG %s :Please provide something to append to the topic\r\n" % (channel))
			if sData.startswith('!topictrim '):
				try:
					query = " | " + sData.split("!topictrim ")[1].strip() 
					topic = topic.replace(query, "")
					send(s, "TOPIC %s :%s\r\n" % (channel, topic))
				except Exception as e:
					send(s, "PRIVMSG %s :Query not found\r\n" % [channel])
					pass
			if sData.startswith('!currenttopic'):
				send(s, "PRIVMSG %s :%s\r\n" % (channel, topic))
			if sData.startswith('!topicappend'):
				try:
					append = sData.split('!topicappend ')[1].strip()
					print append
					#topic = open("current_topic").read().strip().split("\n")[0]
					send(s, "TOPIC %s :%s\r\n" % (channel, topic.strip()+" | "+append))
					topic = topic + " | " + append
				except Exception as e:
					print e
					send(s, "PRIVMSG %s :Please provide something to append to the topic\r\n" % (channel))
			if sData.startswith('.todo'):
				try:
					arg = sData.split('.todo ')[1]
					if arg == 'list':
						send(s, "PRIVMSG %s :Todo-list\r\n" % (channel))
						for td in todo_list:
							send(s, "PRIVMSG %s :%s \r\n" % (channel, str(td)))
					if arg.startswith('add'):
						arg = arg.split('add ')[1].strip()
						todo_list.append(arg.strip())
						file = open("todo.py", "w+")
						file.write("todo_list = " + str(todo_list))
						file.close()
						send(s, "PRIVMSG %s :%s added to todo-list\r\n" % (channel, arg))
					if arg.startswith('del'):
						arg = arg.split('del ')[1].strip()
						todo_list.remove(arg.strip())
						file = open("todo.py", "w+")
						file.write("todo_list = " + str(todo_list))
						file.close()
						send(s, "PRIVMSG %s :%s deleted from todo-list\r\n" % (channel, arg))
				except Exception as e:
					send(s, "PRIVMSG %s :Please provide a valid subject to append to the todo-list\r\n" % (channel))
					
Net()
