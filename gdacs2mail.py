import schedule
import time
import feedparser
import smtplib

### GeoRSS
GDACS = 'http://www.gdacs.org/xml/rss.xml'
COPERNICUS_RAPID_MAPPING = 'http://emergency.copernicus.eu/mapping/activations-rapid/feed'
EONET = 'https://eonet.sci.gsfc.nasa.gov/api/v2.1/events/rss'
NOAA_TSUNAMI = 'https://ptwc.weather.gov/feeds/ptwc_rss_pacific.xml'

RSS_URLS = [GDACS] #not tested [GDACS,EONET,NOAA_TSUNAMI,COPERNICUS_RAPID_MAPPING]

feeds = []

def job():
	for url in RSS_URLS:
		feeds.append(feedparser.parse(url))

	for feed in feeds:
	    for post in feed.entries:
	    	t = post.title
	    	l = post.link
	    	d = post.description
	        w = post.where
	        g = post.guid
    		print t,g,d,l,w + '\n'
	        s = smtplib.SMTP('smtp.gmail.com', 587)
	        s.starttls()
	        s.login("your.gmail.server@gmail.com", "password")
	        msg = d
	        sender = 'your.gmail.server@gmail.com'
	        recipients = ['recipient1@gmail.com', 'recipent2@gmail.com]
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
