import re
import urllib
import socket
import twitter
import dns.resolver
import urllib2
import threading
import json
import random
import os
from datetime import datetime
from access import access_list
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller

#Skype API
class SkypeResolver(threading.Thread):
	
        def ResolveIP(self, user):
                post_vars = {
						"resolve": "Grab IP",
						"skypeName": user
                }
                try:
						reponse = urllib2.urlopen("http://strikeread.ml/api/apiskyper.php?username="+user).read()
						q = reponse.split("\n")[0]
						return q
                except(ValueError, IndexError):
					pass
					
#Bot commands
def help(s, name):
	s.send('PRIVMSG ' + name + ' :-----Help Menu-----\r\n')
	s.send('PRIVMSG ' + name + ' :.ip <site> - Get ip of site\r\n')
	s.send('PRIVMSG ' + name + ' :.ipv6 <site> - Get ipv6 of website\r\n')
	s.send('PRIVMSG ' + name + ' :!tweet <message> - Send a tweet\r\n')
	s.send('PRIVMSG ' + name + ' :!deltweet <message-id> - Delete tweet\r\n')
	s.send('PRIVMSG ' + name + ' :To get message ID visit this page http://www.redgage.com/blogs/tiggerfan/how-to-find-a-tweet-id-on-twitter.html\r\n')
	s.send('PRIVMSG ' + name + ' :.ping <optional-site> - Test your connection or ping website\r\n')
	s.send('PRIVMSG ' + name + ' :.cf <site> - Resolves cloud flare domains\r\n')
	s.send('PRIVMSG ' + name + ' :!ryan - check how long Ryan has been in prison\r\n')
	s.send('PRIVMSG ' + name + ' :!news - get latest news headlines\r\n')
	s.send('PRIVMSG ' + name + ' :.quotes <user> - List a users quotes\r\n')
	s.send('PRIVMSG ' + name + ' :.quoteadd <user> <quote> - Add quote to user\r\n')
	s.send('PRIVMSG ' + name + ' :.quotedel - Delete a quote. Only authorized users can do this.\r\n')
	s.send('PRIVMSG ' + name + ' :.quoterand - Get three random quotes\r\n')
	s.send('PRIVMSG ' + name + ' :!reddit - Load the latest reddit homepage and get the first post\r\n')
	s.send('PRIVMSG ' + name + ' :!nextpost - Get next reddit post\r\n')
	s.send('PRIVMSG ' + name + ' :!subreddit <topic> - Load the latest subreddit post\r\n')
	s.send('PRIVMSG ' + name + ' :.urbandic <word> - Get definition of a word using urban dictionary\r\n')
	s.send('PRIVMSG ' + name + ' :.topic - Get the bot topic\r\n')
def send(s, msg):
	s.send(msg)
def sendTweet(s, name, message, channel):
	api = twitter.Api()
	api = twitter.Api(consumer_key='0gC5kN2x8IhLulOB2hIKl3Opg',
	consumer_secret='zw9Ijo54LfRhg2vWQ8LIEgvgZu7hSBmkUHdKkYqpyp2gZD5Y5V', access_token_key='2953230724-LAkaaQNvwTDru4h3sImJLeF8gXfi85alIK9Ovdl', access_token_secret='PNU3G0JfbLbXkDU1E5raTnLhU0AcwCcPyFnpTVYnghipD') 
	try:
		status = api.PostUpdate(message)
		s.send('PRIVMSG ' + channel + ' :Your message has been tweeted \r\n')
		f = open("tweets.txt", "a+")
		f.write("Name:"+name+ " : " + message+"\n")
		f.close()
	except(e):
		s.send('PRIVMSG ' + channel + ' :Duplicate message\r\n')

def sendReTweet(s, name, msgid, channel):
	if name.strip() in access_list:
		message = msgid
		api = twitter.Api()
		api = twitter.Api(consumer_key='0gC5kN2x8IhLulOB2hIKl3Opg',
		consumer_secret='zw9Ijo54LfRhg2vWQ8LIEgvgZu7hSBmkUHdKkYqpyp2gZD5Y5V', access_token_key='2953230724-LAkaaQNvwTDru4h3sImJLeF8gXfi85alIK9Ovdl', access_token_secret='PNU3G0JfbLbXkDU1E5raTnLhU0AcwCcPyFnpTVYnghipD') 
		try:
			status = api.PostRetweet(int(message))
			s.send('PRIVMSG ' + channel + ' :Tweet has been retweeted \r\n')
		except Exception as e :
			s.send('PRIVMSG ' + channel + ' :Tweet not found or ID incorrect\r\n')
			s.send('PRIVMSG ' + channel + ' :Python error:' + str(e) + '\r\n')
		
def deleteTweet(s, name, msgid, channel):
	if name.strip() in access_list:
		message = msgid
		api = twitter.Api()
		api = twitter.Api(consumer_key='0gC5kN2x8IhLulOB2hIKl3Opg',
		consumer_secret='zw9Ijo54LfRhg2vWQ8LIEgvgZu7hSBmkUHdKkYqpyp2gZD5Y5V', access_token_key='2953230724-LAkaaQNvwTDru4h3sImJLeF8gXfi85alIK9Ovdl', access_token_secret='PNU3G0JfbLbXkDU1E5raTnLhU0AcwCcPyFnpTVYnghipD') 
		try:
			status = api.DestroyStatus(int(message))
			s.send('PRIVMSG ' + channel + ' :Your tweet has been deleted \r\n')
		except Exception as e :
			s.send('PRIVMSG ' + channel + ' :Tweet not found or ID incorrect\r\n')
			s.send('PRIVMSG ' + channel + ' :Python error:' + str(e) + '\r\n')
			
def news(s, channel):
	problem_url  = "http://www.nydailynews.com/"
	problem_page = urllib2.urlopen(problem_url)
	soup = BeautifulSoup(problem_page.read())
	problem_text = soup.find("h2").text
	print problem_text.strip()
	s.send('PRIVMSG ' + channel + ' :Top headline - ' + problem_text.strip().encode('utf8')+ '\r\n')

def pingIp(s, site, channel):
	t = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",site)
	if (t):
		p = socket.gethostbyname(site)
		socket.gethostbyaddr(p)
		s.send('PRIVMSG ' + channel + ' :'+site + ' with ip ' + p + ' - is up\r\n')
		
def pingSite(s, site, channel):
	q = urllib.urlopen("http://"+site).getcode()
	print q
	if q == 200 or q == 403:
		p = socket.gethostbyname(site)
		s.send('PRIVMSG ' + channel + ' :'+site + ' with ip ' + p + ' - is up\r\n')
		
def getIp(s, site, channel):
	ip = socket.gethostbyname(site)
	if site == "rile5.com":
		s.send('PRIVMSG ' + channel + ' :' + site + "'s ip is - 198.57.47.136\r\n")	
	else:
		s.send('PRIVMSG ' + channel + ' :' + site + "'s ip is - " + ip + "\r\n")

def getIpv6(s, site, channel):
	ipv6 = dns.resolver.query(site, "AAAA")
	s.send('PRIVMSG ' + channel + ' :' + site + "'s ipv6 is - " + str(ipv6[0]) + "\r\n")

def access(s, name, channel, data):
	if name.strip() == "list":
		s.send('PRIVMSG ' + channel + ' :Access list: '+ str(access_list) +'\r\n')
	if "add" in name.strip():
		name = data.split('add ')[1]
		access_list.append(name.strip())
		s.send('PRIVMSG ' + channel + ' :User added to access list\r\n')
		f = open("access.py", "w+")
		f.write("access_list = " + str(access_list))
		f.close()
	if "del" in name.strip():
		name = data.split('del ')[1]
		if(name.strip() in access_list):
			access_list.remove(name.strip())
			s.send('PRIVMSG ' + channel + ' :User deleted from access list\r\n')
			f = open("access.py", "w+")
			f.write("access_list = " + str(access_list))
			f.close()
		else:
			s.send('PRIVMSG ' + channel + ' :User not in access list\r\n')	
def fuck(s, channel):
	s.send('PRIVMSG ' + channel + ' :Fuck her right in the pussy\r\n')		
def cloudFlareResolver(s, site, channel):
                try:
						reponse = urllib2.urlopen("http://api.cloudsolve.in/?domain="+site).read()
						q = reponse.split("\n")[0]
						s.send('PRIVMSG ' + channel + ' :' + site + ' resolved ip - ' + q +'\r\n')	
						return q
                except(ValueError, IndexError):
					pass	
def ryan(s, channel):
	start_date = 'Wed Dec 30 3:00:0 +0000 2014'
	end_date = datetime.today()
	start = __datetime(start_date)
	end = end_date
	delta = end - start
	s.send('PRIVMSG ' + channel + ' :Ryan has been in prison for '+ str(delta).split(",")[0] + '\r\n')

def geoIP(s, ip, channel):
	try:
		reponse = urllib2.urlopen("http://ip-api.com/json/"+ip).read()
		ip_info = reponse.strip()
		ip_info = json.loads(ip_info)
		print(ip_info)
		if(ip_info['status'] == 'fail'):
			s.send("PRIVMSG %s :Failed to find information on IP\r\n" % (channel))
		#print ip_info
		#s.send('PRIVMSG %s : %s - %s\r\n' % (channel, ip_info)
		else:
			s.send('PRIVMSG %s :%s - %s, %s, %s, %s, %s, TimeZone: %s, Owner: %s\r\n' % (channel, ip, ip_info['city'], ip_info['regionName'], ip_info['zip'], ip_info['country'], ip_info['isp'], ip_info['timezone'], ip_info['as'] ))
	except(ValueError, IndexError):
		s.send('PRIVMSG %s : Could not get IP information\r\n' % (channel))
		pass


#Reddit config		
global reddit_topics
reddit_topics = []
global rCounter #Stores the number of which topic you are on
rRounter = 0
def reddit(s, channel, *args):
	if len(args) > 0:
			url = "http://reddit.com/r/"+args[0]
	else:
		url = "http://reddit.com"
	page = urllib2.Request(url, headers={ 'User-Agent' : 'Iris by /u/Iris' })
	page = urllib2.urlopen(page)
	results = BeautifulSoup(page.read())
	posts = results.find_all("div", {"class":"entry unvoted"})
	print posts
	global reddit_topics
	reddit_topics = []
	reddit_topics = posts
	global rCounter
	rCounter = 0
	send(s, "PRIVMSG %s :%s\r\n" % (channel, str(reddit_topics[0].a.contents[0]).encode("ascii")))
	if str(reddit_topics[0].a['href']).encode("ascii").startswith("/r/"):
		send(s, "PRIVMSG %s :%s\r\n" % (channel, "http://reddit.com"+str(reddit_topics[0].a['href']).encode("ascii")))
	else:
		send(s, "PRIVMSG %s :%s\r\n" % (channel, str(reddit_topics[0].a['href']).encode("ascii"))) 
	
def reddit_next(s, channel):
	if "rCounter" in globals():
		global rCounter
		rCounter += 1
		global reddit_topics
		send(s, "PRIVMSG %s :%s\r\n" % (channel, str(reddit_topics[rCounter].a.contents[0]).encode("ascii")))
		if str(reddit_topics[0].a['href']).encode("ascii").startswith("/r/"):
			send(s, "PRIVMSG %s :%s\r\n" % (channel, "http://reddit.com"+str(reddit_topics[rCounter].a['href']).encode("ascii")))
		else:
			send(s, "PRIVMSG %s :%s\r\n" % (channel, str(reddit_topics[rCounter].a['href']).encode("ascii"))) 
	else:
		send(s, "PRIVMSG %s :Please pick a topic first using !reddit <topic>\r\n" % (channel))
#Tools
def __datetime(date_str):
	return datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
	
def user(msg):
	name = msg[1:].split("!")[0]
	print name
	return str(name)

def whois(s, name):
	s.send("WHOIS " + name + "\r\n")
	f = s.recv(1048)
	print f
	if f.find("Iris " + name + " " + name + " :is logged in as") != -1:
		return True
	else:
		return False

def NewTorIP():
	with Controller.from_port(port = 9051) as controller:
		controller.authenticate()
		controller.signal(Signal.NEWNYM)
		
def quoteAdd(s, channel, user, quote):
	quote = quote
	user = user
	if os.path.isfile(user + '.txt'):
		f = open(user + '.txt', 'a+')
		f.write('"' + quote + '"\n')
		f.close()
		f = open('quotes.txt', 'a+')
		f.write(user + ' "' + quote + '"\n')
		f.close()
		send(s, "PRIVMSG %s :Quote was added!\r\n" % (channel))
	else:
		f = open(user + '.txt', 'w')
		f.close()
		f = open(user + '.txt', 'a+')
		f.write('"' + quote + '"\n')
		f.close()
		f = open('quotes.txt', 'a+')
		f.write(user + ' "' + quote + '"\n')
		f.close()
		send(s, "PRIVMSG %s :Quote was added!\r\n" % (channel))


def newestquote(s, channel):
	f = open('quotes.txt', 'r')
	read = f.read()
	split_text = read.split('\n')
	join_text = ''.join(split_text)
	if join_text == '':
		s.send('PRIVMSG ' + channel + ' :Please enter a quote first!\r\n')
	else:
		s.send('PRIVMSG ' + channel + ' :' + split_text[-2] + '\r\n')
def quotedel(s, channel, user, quote):
	user = user
	quote = quote
	f = open(user + '.txt', 'r')
	lines = f.readlines()
	f.close()
	f = open(user + '.txt', 'w')
	for line in lines:
		if line != '"'+quote+'"\n':
			f.write(line)
		else:
			pass
	f = open('quotes.txt', 'r')
	lines = f.readlines()
	f.close()
	f = open('quotes.txt', 'w')
	for line in lines:
		if line != user +' "'+quote+'"\n':
			f.write(line)
		else:
			pass
	s.send('PRIVMSG ' + channel + ' :Quote deleted!\r\n')
	f.close()

def urbandic(s, channel, word):
	word = word
	url = ("http://www.urbandictionary.com/define.php?term="+word)
	openurl = urllib2.urlopen(url)
	try:
		soup = BeautifulSoup(openurl.read())
		findtag = soup.find('div', {'class':'meaning'}).text
		send(s, "PRIVMSG %s :%s\r\n" % (channel, findtag.strip().encode('utf8')))
	except Exception as e:
		send(s, "PRIVMSG %s :Could not find a definition for %s\r\n" % (channel, word))
		pass

def listquotes(s, channel):
	f = open('Iris.txt', 'r')
	read = f.read()
	split = read.split('\n')
	send(s, "PRIVMSG %s :%s\r\n" % (channel, (random.choice(split))))
	send(s, "PRIVMSG %s :%s\r\n" % (channel, (random.choice(split))))
	send(s, "PRIVMSG %s :%s\r\n" % (channel, (random.choice(split))))
	
def topic(s, channel):
	f = open('topic.txt', 'r')
	read = f.read()
	split = read.split('\n')
	send(s, "PRIVMSG %s :%s\r\n" % (channel,split[0]))

def topicadd(s, channel, topic):
	f = open('topic.txt', 'w')
	write = f.write('Iris - By niggerbread and Luga | '+topic)
	f.close()

def topicappend(s, channel, topic):
	myFile = open('topic.txt', 'a+')
	myFile.write(" | " + topic)
	myFile.close()

def quoterand(s, channel):
	f = open('quotes.txt', 'r')
	read = f.read()
	split = read.split('\n')
	send(s, "PRIVMSG %s :%s\r\n" % (channel, (random.choice(split))))

def quotes(s, channel, person):
	theuser = person
	if os.path.isfile(theuser + '.txt'):
		f = open(theuser + '.txt', 'r')
		read = f.read()
		quoteslist = read.split('\n')
		quoteslist = ', '.join(quoteslist)
		quoteslist = quoteslist.rstrip(', ')
		if quoteslist == '':
			send(s, "PRIVMSG %s :Please add quotes for this user first!\r\n" % (channel))
		else:
			send(s, "PRIVMSG %s :%s\r\n" % (channel, quoteslist))
	else:
		send(s, "PRIVMSG %s :Please add quotes for this user first!\r\n" % (channel))

def google(s, channel, request):	
	try:
		page = urllib2.Request("http://google.com/search?client=ubuntu&hs=Ty8&channel=fs&q="+request.replace(" ", "+").strip(), headers={'User-agent' : 'Mozilla/5.0'})
		request = urllib2.urlopen(page)
		request = BeautifulSoup(request.read())
		title = request.find("h3", {"class" : "r"}).text
		send(s, "PRIVMSG %s :%s\r\n" % (channel, title))
		url = request.find("div", {"class" : "kv"}).cite.text
		send(s, "PRIVMSG %s :%s\r\n" % (channel, url))
		desc = request.find("span", {"class" : "st"}).text
		send(s, "PRIVMSG %s :%s\r\n" % (channel, desc))
	except Exception as e:
		send(s, "PRIVMSG %s :Request throttled by shitty tor node\r\n" % (channel))
		
#4chan config	
global fourchan_topics
fourchan_topics = []
global fourchan_names
fourchan_names = []
global fourchan_dates
fourchan_dates = []
global fourchan_messages
fourchan_messages = []
global fourchan_urls
fourchan_urls = []
global fCounter #Stores the number of which topic you are on
fRounter = 0
def fourchan(s, channel, request):
	global fCounter
	board = "/"+request+"/"
	page = urllib2.Request("http://4chan.org"+ board, headers={'User-agent' : 'Mozilla/5.0'})
	request = urllib2.urlopen(page)
	request = BeautifulSoup(request.read())
	details = request.find_all("div", {"class" : "thread"})
	global fourchan_topics
	fourchan_topics = details
	print details
	print "printed details"
	name = details[0].find_all("span", {"class" : "name"})
	print name
	send(s, "PRIVMSG %s :%s\r\n" % (channel, name[0].text))
	date = details[0].find_all("span", {"class" : "dateTime"})
	print date
	send(s, "PRIVMSG %s :%s\r\n" % (channel, date[0].text))
	url = details[0].a['href']
	print url
	send(s, "PRIVMSG %s :%s\r\n" % (channel, "http://boards.4chan.org"+board+url))
	problem_text = details[0].find_all("blockquote",{"class":"postMessage"})
	print problem_text
	send(s, "PRIVMSG %s :%s\r\n" % (channel, problem_text[0].text))
	fCounter = 0
	global current_board
	current_board = board
def fourchannext(s, channel):
	global fourchan_topics
	global current_board
	global fCounter
	fCounter += 1
	send(s, "PRIVMSG %s :%s\r\n" % (channel, fourchan_topics[fCounter].find_all("span", {"class" : "name"})[0].text))
	send(s, "PRIVMSG %s :%s\r\n" % (channel, fourchan_topics[fCounter].find("span", {"class" : "dateTime"}).text))
	send(s, "PRIVMSG %s :%s\r\n" % (channel, "http://boards.4chan.org"+current_board+fourchan_topics[fCounter].a['href']))
	send(s, "PRIVMSG %s :%s\r\n" % (channel, fourchan_topics[fCounter].find("blockquote",{"class":"postMessage"}).text))
