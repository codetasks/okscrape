################
## OKCupid Username Enumerator
## Fetches 1000 usernames for each age per category (eg. 20yr old straight women)
## Requires paid OKCupid account
## Created by Kyle LePrevost
################


#Let's import some modules
import urllib
import urllib2
import re
import cookielib
import time
import os
from bs4 import BeautifulSoup
from urllib2 import urlopen
from random import randint
from time import sleep
import requests
import datetime
import tinys3 
 
#Let's grab the current date
now = datetime.datetime.now()
 
#User credentials
username_input = "editme"
password_input = "editme"
path_input = "dupes-usernames-"+ now.strftime("%Y-%m-%d") + ".csv"
path_input2 = "usernames-"+ now.strftime("%Y-%m-%d") + ".csv"

#Defining some variables
user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'}
credentials = {'username': username_input, 'password': password_input, 'dest': '/home'}

#Start a session with OKCupid
sesh = requests.Session()
login_resp = sesh.post('https://www.okcupid.com/login', data=credentials, headers = user_agent)

#Open the file we want to write to
results = open(path_input, 'a')

#Start the loop for straight women
i=20
while i<27:
	OKCURL_straightchicks = "http://www.okcupid.com/match?filter1=0,34&filter2=2,"+str(i)+","+str(i)+"&filter3=3,25&filter4=5,604800&filter5=1,1&locid=0&timekey=1&matchOrderBy=RANDOM&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count=1000"
	print OKCURL_straightchicks
	match_html_straightchicks = sesh.get(OKCURL_straightchicks, headers = user_agent)
	soup = BeautifulSoup(match_html_straightchicks.text, "lxml")
	usernames = [a.text for a in soup.findAll('a', attrs={'class': 'name ajax_load_profile_link'})]
	for u in usernames:
		results.write(u.encode('utf8')+'\n')
	print(str(len(usernames))+" "+str(i)+" y/o Straight Chicks Found")
	i+=1	
	sleep(randint(2,6))
results.close()

# Start the loop for gay women	
itwo=18
while itwo<40:
	OKCURL_gaychicks = "http://www.okcupid.com/match?filter1=0,40&filter2=2,"+str(itwo)+","+str(itwo)+"&filter3=3,25&filter4=5,2678400&filter5=1,1&locid=0&timekey=1&matchOrderBy=RANDOM&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count=1000"
	print OKCURL_gaychicks
	match_html_gaychicks = sesh.get(OKCURL_gaychicks, headers = user_agent)
	soup = BeautifulSoup(match_html_gaychicks.text, "lxml")
	usernames = [a.text for a in soup.findAll('a', attrs={'class': 'name ajax_load_profile_link'})]
	for u in usernames:
		results.write(u.encode('utf8')+'\n')
	print(str(len(usernames))+" "+str(itwo)+" y/o Gay Chicks Found")
	itwo+=1	
	sleep(randint(5,10))

# Start the loop for straight guys
ithree=18
while ithree<35:
	OKCURL_straightguys = "http://www.okcupid.com/match?filter1=0,17&filter2=2,"+str(ithree)+","+str(ithree)+"&filter3=3,25&filter4=5,2678400&filter5=1,1&locid=0&timekey=1&matchOrderBy=RANDOM&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count=1000"
	print OKCURL_straightguys
	match_html_straightguys = sesh.get(OKCURL_straightguys, headers = user_agent)
	soup = BeautifulSoup(match_html_straightguys.text, "lxml")
	usernames = [a.text for a in soup.findAll('a', attrs={'class': 'name ajax_load_profile_link'})]
	for u in usernames:
		results.write(u.encode('utf8')+'\n')
	print(str(len(usernames))+" "+str(ithree)+" y/o Straight Guys Found")
	ithree+=1	
	sleep(randint(5,10))
	
# Start the loop for gay men		
ifour=18
while ifour<40:
	OKCURL_gayguys = "http://www.okcupid.com/match?filter1=0,20&filter2=2,"+str(ifour)+","+str(ifour)+"&filter3=3,25&filter4=5,2678400&filter5=1,1&locid=0&timekey=1&matchOrderBy=RANDOM&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count=1000"
	print OKCURL_gayguys
	match_html_gayguys = sesh.get(OKCURL_gayguys, headers = user_agent)
	soup = BeautifulSoup(match_html_gayguys.text, "lxml")
	usernames = [a.text for a in soup.findAll('a', attrs={'class': 'name ajax_load_profile_link'})]
	for u in usernames:
		results.write(u.encode('utf8')+'\n')
	print(str(len(usernames))+" "+str(ifour)+" y/o gay dudes Found")
	ifour+=1	
	sleep(randint(5,10))

# Start the loop for straight women
i=20
while i<27:
	OKCURL_straightchicks = "http://www.okcupid.com/match?filter1=0,34&filter2=2,"+str(i)+","+str(i)+"&filter3=3,25&filter4=5,604800&filter5=1,1&locid=0&timekey=1&matchOrderBy=RANDOM&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count=600"
	print OKCURL_straightchicks
	match_html_straightchicks = sesh.get(OKCURL_straightchicks, headers = user_agent)
	soup = BeautifulSoup(match_html_straightchicks.text, "lxml")
	usernames = [a.text for a in soup.findAll('a', attrs={'class': 'name ajax_load_profile_link'})]
	age = [span.text for span in soup.findAll('span', attrs={'class': 'age'})]
	match = [span.text for span in soup.findAll('span', attrs={'class': 'percentage'})]
	for u in usernames:
		results.write(u.encode('utf8')+'\n')
	print(str(len(usernames))+" "+str(i)+" y/o Straight Chicks Found")
	i+=1	
	sleep(randint(2,6))

# Remove Duplicate usernames if any

infile = open(path_input, "r")
outfile = open(path_input2, "w")
listlines = [] # holds lines already seen
for line in infile:
	if line in listlines:
		continue
	else:
		outfile.write(line)
		listlines.append(line)
infile.close()
outfile.close()


#AWS S3 Storage
# Creating a simple connection
conn = tinys3.Connection('S3 Account','S3 Secret',default_bucket='cupidscrape-usernames', endpoint='s3-us-west-2.amazonaws.com', tls='True')

# Uploading a single file
f = open(path_input2,'rb')
conn.upload(path_input2,f)
f.close()
print "Upload to S3 Complete"