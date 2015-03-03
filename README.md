OKScrape
============

For more information, visit my blog detailing this code here:
http://hardcidr.com/okcupid-hacking-for-more-efficient-dating/

# Usage:
**You will need:**
- An OKCupid Premium account
- A second throwaway OKCupid account
- An Amazon S3 bucket

The throwaway account needs to have ONLY the ten questions you want scraped answered. 


**Edit these files**
Username_scraper.py:
- Enter the credentials to your paid OKCupid account here. You can mess with the URL if you don't want to pay for OKC.
- Also add your credentials for S3 at the end of this script.
- Comment out the usernames you don't want scraped. They are grouped by gender/orientation. You can also tune the age range by messing with the value of i in the loop.

profile_grabber_10q.py
- Enter your throwaway account creds
- Add your S3 details
- Edit the question IDs found in the middle of the script to match what the questions you WANT to scrape. You will need to answer these questions in the throwaway account to scrape them from the accounts of others.
- Edit the weights appropriately. 

