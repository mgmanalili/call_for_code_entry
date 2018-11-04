import schedule
import time
import feedparser
import smtplib

### GeoRSS
gdacs_geo = 'http://www.gdacs.org/xml/gdacs_cap.xml' #V2
gdacs_main = 'http://www.gdacs.org/xml/rss.xml' #v2 has attrib where

RSS_URLS = [gdacs_main]

feeds = []

def job():
	for url in RSS_URLS:
		feeds.append(feedparser.parse(url))

	for feed in feeds:
	    for post in feed.entries:
	    	a = post.title
	    	b = post.link
	    	c = post.description
	        #w = post.where
	        g = post.guid
    		print a,b,c,g + '\n'
	        s = smtplib.SMTP('smtp.gmail.com', 587)
	        s.starttls()
	        s.login("your.other.account@gmail.com", "password")
	        msg = a
	        sender = 'your.other.account@gmail.com'
	        recipients = ['reciever.email@gmail.com']
	        s.sendmail(sender, recipients, str(msg))
	        s.quit()

#schedule.every(10).seconds.do(job)
schedule.every(24).hours.do(job)

while 1:
	schedule.run_pending()
	time.sleep(1)

#https://www.youtube.com/watch?v=D-NYmDWiFjU
#Sign in to gmail > settings (gear) > settings > Forward and POP/IMAP > Enable IMAP > save
#Sign in and security > very buttom > check allow less secure apps ON
