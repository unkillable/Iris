import re
import urllib
import socket
import twitter
import dns.resolver
import urllib2
import threading
import json
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
