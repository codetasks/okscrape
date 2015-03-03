#################################
## OKCupid Profile Data Scraper
## Reads usernames from usernames.csv
## Created by Kyle LePrevost
#################################

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
 
#Fetch user credentials
#username_input = raw_input("Enter your OKCupid Username: ")
#password_input = raw_input("Enter your OKCupid Password: ")
 
 #Let's grab the current date
now = datetime.datetime.now()

#Defining some variables
user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'}
credentials = {'username': 'editme', 'password': 'editme', 'dest': '/home'}
usernames_file = "usernames-"+ now.strftime("%Y-%m-%d") + ".csv"
database = "profiles-"+ now.strftime("%Y-%m-%d") + ".csv"


# Get Files
conn = tinys3.Connection('S3 Account','S3 Secret', endpoint='s3-us-west-2.amazonaws.com', tls='True')
usernamedl = urllib.URLopener()
usernamedl.retrieve("S3 URL"+usernames_file, usernames_file)


#Start a session with OKCupid
sesh = requests.Session()
login_resp = sesh.post('https://www.okcupid.com/login', data=credentials, headers = user_agent)

#Open the usernames file
open_usernames = open(usernames_file, 'r')
usernames = open_usernames.readlines() 
open_database = open(database, 'a')

# Start the loop
# Set i to the starting place in your usernames list
# Good for resuming failed or interrupted sessions
i=0
while i<len(usernames):
	OKCURL = "http://www.okcupid.com/profile/"+ usernames[i].strip() +"?cf=regular"
	# Let's download the HTML file (sesh.get) of OKCURL with the correct user agent. Save to match_html
	match_html = sesh.get(OKCURL, headers = user_agent)
	# Take HTML, convert to text, and pass into a BS4 instance called "soup"
	soup = BeautifulSoup(match_html.text, "lxml")
	# Read the title of the web page
	title = soup.html.head.title
	# Let's skip deleted accounts up front
	if title.string == "OkCupid |  Account not found":
		print "Account Not Found"
		i+=1
	else:
		# Scrape the basic profile data and save it to profile record
		name = [span.text for span in soup.findAll('span', attrs={'class': 'name '})]
		# Alright, we have all the setup work done. Let's print the username to terminal for debugging
		print name[0]+" profile being scraped"
		age = [span.text for span in soup.findAll('span', attrs={'id': 'ajax_age'})]
		orientation = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_orientation'})]
		gender = [span.text for span in soup.findAll('span', attrs={'class': 'ajax_gender'})]
		status = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_status'})]
		location = [span.text for span in soup.findAll('span', attrs={'id': 'ajax_location'})]
		ethnicity = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_ethnicities'})]
		height = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_height'})]
		bodytype = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_bodytype'})]
		diet = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_diet'})]
		smokes = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_smoking'})]
		drinks = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_drinking'})]
		drugs = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_drugs'})]
		religion = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_religion'})]
		sign = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_sign'})]
		education = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_education'})]
		job = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_job'})]
		income = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_income'})]
		offspring = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_children'})]
		pets = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_pets'})]
		languages = [dd.text for dd in soup.findAll('dd', attrs={'id': 'ajax_languages'})]
		self_summary = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_0'})]
		doing = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_1'})]
		good = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_2'})]
		notice = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_3'})]
		favs = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_4'})]
		without = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_5'})]
		thinking = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_6'})]
		friday = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_7'})]
		private = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_8'})]
		message = [div.text for div in soup.findAll('div', attrs={'id': 'essay_text_9'})]
		wants = [li.text for li in soup.findAll('li', attrs={'id': 'ajax_gentation'})]
		age_range = [li.text for li in soup.findAll('li', attrs={'id': 'ajax_ages'})]
		lookingfor = [li.text for li in soup.findAll('li', attrs={'id': 'ajax_lookingfor'})]
		# Clean up the information sections to remove extra commas (breaks the CSV db)	
		income_san = income[0].replace(',',' ')
		pets_san = pets[0].replace(',',' ')
		ethnicity_san = ethnicity[0].replace(',',' ')
		religion_san = religion[0].replace(',',' ')
		sign_san = sign[0].replace(',',' ')
		offspring_san = offspring[0].replace(',',' ')
		languages_san = languages[0].replace(',',' ')
		education_san = education[0].replace(',',' ')
		# Clean up the essay sections to remove line breaks and commas. Again, breaks the CSV format otherwise.
		# Yes, I know I'm lazy for not using a sqlitedb
		if self_summary:
			self_summary_san1 = self_summary[0].replace(',',' ')
			self_summary_san2 = self_summary_san1.replace('\n',' ')
		if doing:
			doing_san1 = doing[0].replace(',',' ')
			doing_san2 = doing_san1.replace('\n',' ')
		if good:
			good_san1 = good[0].replace(',',' ')
			good_san2 = good_san1.replace('\n',' ')
		if notice:
			notice_san1 = notice[0].replace(',',' ')
			notice_san2 = notice_san1.replace('\n',' ')
		if favs:
			favs_san1 = favs[0].replace(',',' ')
			favs_san2 = favs_san1.replace('\n',' ')
		if without:
			without_san1 = without[0].replace(',',' ')
			without_san2 = without_san1.replace('\n',' ')
		if thinking:
			thinking_san1 = thinking[0].replace(',',' ')
			thinking_san2 = thinking_san1.replace('\n',' ')
		if friday:
			friday_san1 = friday[0].replace(',',' ')
			friday_san2 = friday_san1.replace('\n',' ')
		if private:
			private_san1 = private[0].replace(',',' ')
			private_san2 = private_san1.replace('\n',' ')
		if message:
			message_san1 = message[0].replace(',',' ')
			message_san2 = message_san1.replace('\n',' ')
		if wants:
			wants_san1 = wants[0].replace(',',' ')
			wants_san2 = wants_san1.replace('\n',' ')
		if lookingfor:
			lookingfor_san1 = lookingfor[0].replace(',',' ')
			lookingfor_san2 = lookingfor_san1.replace('\n',' ')
		#Time to dump some data in the CSV
		open_database.write(name[0].encode('utf8')+',')
		open_database.write(gender[0].encode('utf8')+',')
		open_database.write(age[0].encode('utf8')+',')
		open_database.write(orientation[0].encode('utf8')+',')
		open_database.write(status[0].encode('utf8')+',')
		open_database.write(location[0].encode('utf8')+',')
		open_database.write(ethnicity_san.encode('utf8')+',')
		open_database.write(height[0].encode('utf8')+',')
		open_database.write(bodytype[0].encode('utf8')+',')
		open_database.write(diet[0].encode('utf8')+',')
		open_database.write(smokes[0].encode('utf8')+',')
		open_database.write(drinks[0].encode('utf8')+',')
		open_database.write(drugs[0].encode('utf8')+',')
		open_database.write(religion_san.encode('utf8')+',')
		open_database.write(sign_san.encode('utf8')+',')
		open_database.write(education[0].encode('utf8')+',')
		open_database.write(job[0].encode('utf8')+',')
		open_database.write(income_san.encode('utf8')+',')
		open_database.write(offspring_san.encode('utf8')+',')
		open_database.write(pets[0].encode('utf8')+',')
		open_database.write(languages_san.encode('utf8')+',')
		# Essay sections be all special-like again - sometimes folks don't fill them out
		# We need to check that and write null if nothing exists
		if self_summary:
			open_database.write(self_summary_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if doing:
			open_database.write(doing_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if good:
			open_database.write(good_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if notice:
			open_database.write(notice_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if favs:
			open_database.write(favs_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if without:
			open_database.write(without_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if thinking:
			open_database.write(thinking_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if friday:
			open_database.write(friday_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if private:
			open_database.write(private_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if message:
			open_database.write(message_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if wants:
			open_database.write(wants_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		if lookingfor:
			open_database.write(lookingfor_san2.encode('utf8')+',')
		else:
			open_database.write('null'.encode('utf8')+',')
		# Set the URLs we want to download question data from. 
		OKCURL2 = "http://www.okcupid.com/profile/"+ usernames[i].strip() +"/questions?i_care=1"
		# Download the raw HTML for these pages to memory
		match_html2 = sesh.get(OKCURL2, headers = user_agent)
		# This section is absolutely fucked. Needs fixing.
		# Pretty much we want to check if they answered a question we are interested in
		# Then write the answer to our CSV after stripping those damn commas
		soup = BeautifulSoup(match_html2.text, "html")
		# Cats v Dogs
		answer1 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_997'})]
		# Self confidence
		answer2 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_20930'})]		
		# Religion importance
		answer3 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_41'})]		
		# How long relationship last?
		answer4 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_41953'})]		
		# Type of intelligence
		answer5 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_29032'})]		
		# Meet people
		answer6 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_16053'})]		
		# Political Orientation
		answer7 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_212813'})]		
		# Going out vs coming home to?
		answer8 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_20021'})]		
		# Sex frequency
		answer9 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_12605'})]		
		# Dates # before sex
		answer10 = [span.text for span in soup.findAll('span', attrs={'id': 'answer_target_24375'})]		
		answer_san1 = "null"
		if answer1:
			answer_san1 = answer1[0].replace(',',' ')
			open_database.write(answer_san1.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san2 = "null"
		if answer2:
			answer_san2 = answer2[0].replace(',',' ')
			open_database.write(answer_san2.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san3 = "null"
		if answer3:
			answer_san3 = answer3[0].replace(',',' ')
			open_database.write(answer_san3.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san4 = "null"
		if answer4:
			answer_san4 = answer4[0].replace(',',' ')
			open_database.write(answer_san4.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san5 = "null"
		if answer5:
			answer_san5 = answer5[0].replace(',',' ')
			open_database.write(answer_san5.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san6 = "null"
		if answer6:
			answer_san6 = answer6[0].replace(',',' ')
			open_database.write(answer_san6.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san7 = "null"
		if answer7:
			answer_san7 = answer7[0].replace(',',' ')
			open_database.write(answer_san7.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san8 = "null"
		if answer8:
			answer_san8 = answer8[0].replace(',',' ')
			open_database.write(answer_san8.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san9 = "null"
		if answer9:
			answer_san9 = answer9[0].replace(',',' ')
			open_database.write(answer_san9.encode('utf8')+',')
		else:
			open_database.write("null,")
		answer_san10 = "null"			
		if answer10:
			answer_san10 = answer10[0].replace(',',' ')
			open_database.write(answer_san10.encode('utf8')+',')
		else:
			open_database.write("null,")
		#Match Algorithm
		#Zero out lifestyle score "eros"
		EROS = 0
		#Zero out personality score "phileo"
		PHILEO = 0
		#Age
		if " 20 " in age:
			EROS = EROS - 300
		if " 21 " in age:
			EROS = EROS - 100
		if " 22 " in age:
			EROS = EROS + 50
		if " 23 " in age:
			EROS = EROS + 100
		if " 24 " in age:
			EROS = EROS + 50
		if " 25 " in age:
			EROS = EROS - 100
		if " 26 " in age:
			EROS = EROS - 300
		#Location
		if "Henrico, VA" in location:
			EROS = EROS + 100
		if "Glen Allen, VA" in location:
			EROS = EROS + 100
		#Bodytype
		if "Overweight" in bodytype:
			EROS = EROS - 300
		if "Full figured" in bodytype:
			EROS = EROS - 100
		if "Curvy" in bodytype:
			EROS = EROS - 100
		if "A little extra" in bodytype:
			EROS = EROS - 100
		if "Athletic" in bodytype:
			EROS = EROS + 50
		if "Fit" in bodytype:
			EROS = EROS + 50
		if "Jacked" in bodytype:
			EROS = EROS - 100
		if "Average" in bodytype:
			EROS = EROS + 100
		if "Skinny" in bodytype:
			EROS = EROS + 100
		if "Thin" in bodytype:
			EROS = EROS + 100
		#Smoking
		if "Yes" in smokes:
			EROS = EROS - 300
		if "Trying to quit" in smokes:
			EROS = EROS - 300
		if "No" in smokes:
			EROS = EROS + 100
		#Ethnicity
		if "Black" in ethnicity_san:
			EROS = EROS - 100
		if "White" in ethnicity_san:
			EROS = EROS + 100
		#Education
		if "Graduated" in education_san:
			EROS = EROS + 100
		if "high school" in education_san:
			EROS = EROS - 300
		if "Working on university" in education_san:
			EROS = EROS - 300
		if "space camp" in education_san:
			EROS = EROS - 300
		#Job
		if "Student" in job:
			EROS = EROS - 300
		if "Technology" in job:
			EROS = EROS + 100
		if "Science / Engineering" in job:
			EROS = EROS + 100
		#Kids
		if "Has a kid" in offspring_san:
			EROS = EROS - 300
		if "Has kids" in offspring_san:
			EROS = EROS - 300	
		#Religion
		if "Agnosticism" in religion_san:
			EROS = EROS + 100
		if "Atheism" in religion_san:
			EROS = EROS + 100
		if "Catholicism" in religion_san:
			EROS = EROS - 300
		if "Christianity" in religion_san:
			EROS = EROS - 300
		if "Islam" in religion_san:
			EROS = EROS - 300
		if "Judaism" in religion_san:
			EROS = EROS - 300
		#Drugs
		if "Never" in drugs:
			EROS = EROS + 100
		if "Often" in drugs:
			EROS = EROS - 100
		if "Sometimes" in drugs:
			EROS = EROS - 50
		#Drinking
		if "Socially" in drinks:
			EROS = EROS + 100
		if "Very often" in drinks:
			EROS = EROS - 300
		if "Rarely" in drinks:
			EROS = EROS + 50
		#Food
		if "Strictly vegetarian" in diet:
			EROS = EROS - 100
		if "Strictly vegan" in diet:
			EROS = EROS - 100
		if "Vegetarian" in diet:
			EROS = EROS - 100
		if "Vegan" in diet:
			EROS = EROS - 100
		#Pets
		if "Has dogs" in pets_san:
			EROS = EROS - 300
		if "Has cats" in pets_san:
			EROS = EROS + 100
		if "Likes cats" in pets_san:
			EROS = EROS + 100
		if "dislikes cats" in pets_san:
			EROS = EROS - 300
		#Looking For
		if "long-term" in lookingfor_san2:
			PHILEO = PHILEO + 100
		# Cats v Dogs
		if "Cats" in answer_san1:
			PHILEO = PHILEO + 100
		if "Dogs" in answer_san1:
			PHILEO = PHILEO - 100
		#Self Confidence
		if "Average" in answer_san2:
			PHILEO = PHILEO + 100
		if "very" in answer_san2:
			PHILEO = PHILEO - 100
		#Religion importance
		if "Not at all important" in answer_san3:
			PHILEO = PHILEO + 100
		if "Extremely important" in answer_san3:
			PHILEO = PHILEO - 100
		#How long relationship last?
		if "Several years" in answer_san4:
			PHILEO = PHILEO + 100
		if "One night" in answer_san4:
			PHILEO = PHILEO - 300
		if "A few months to a year" in answer_san4:
			PHILEO = PHILEO - 100
		#Type of intelligence
		if "Logical / Mathematical" in answer_san5:
			PHILEO = PHILEO + 100
		# Willing to meet
		if "willing!" in answer_san6:
			PHILEO = PHILEO + 100
		if "interested" in answer_san6:
			PHILEO = PHILEO - 300
		#Political orientation
		if "Liberal / Left-wing" in answer_san7:
			PHILEO = PHILEO + 100
		if "Conservative / Right-wing" in answer_san7:
			PHILEO = PHILEO - 200
		# Going out vs coming home to?
		if "come home" in answer_san8:
			PHILEO = PHILEO + 100
		if "tonight" in answer_san8:
			PHILEO = PHILEO - 200
		#Sex frequency
		if "About every other day" in answer_san9:
			PHILEO = PHILEO + 100
		if "A few times a month or less" in answer_san9:
			PHILEO = PHILEO - 300
		if "Once or twice a week" in answer_san9:
			PHILEO = PHILEO + 25
		if "Every day" in answer_san9:
			PHILEO = PHILEO + 100
		#Dates before sex
		if "3-5 dates" in answer_san10:
			PHILEO = PHILEO + 100
		if "6 or more dates" in answer_san8:
			PHILEO = PHILEO + 50
		if "Only after the wedding" in answer_san8:
			PHILEO = PHILEO - 300
		if "1-2 dates" in answer_san8:
			PHILEO = PHILEO - 100
		EROS = EROS * 2
		AGAPE = PHILEO + EROS
		open_database.write(str(EROS)+',')
		open_database.write(str(PHILEO)+',')
		open_database.write(str(AGAPE)+',')
		open_database.write('\n')
		sleep(randint(1,3))
		i+=1
		print str(i)+" profiles scraped so far"
		
#Upload to AWS		
f = open(database,'rb')		
conn.upload(database,f,'cupidscrape-data')