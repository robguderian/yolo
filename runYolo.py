#!/usr/local/bin/python
from twitter import Twitter, OAuth, TwitterHTTPError
import time, sys, random

OAUTH_TOKEN = ''
OAUTH_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

tweets = ['#yoloswag420everyday', '#YOLO', '#swag', '#420forlife', '#YoLo']
maxDate = 0

def parseDate(datestr):
    #Fri Sep 27 16:53:06 +0000 2013
    return time.strptime(datestr, '%a %b %d %H:%M:%S +0000 %Y')


def getDateFromFile():
    global maxDate
    #Fri Sep 27 16:53:06 +0000 2013
    with open("lastdate.txt", 'r') as f:
        content = f.read().strip()
        maxDate = parseDate(content)
    return maxDate
        
def writeDateToFile(thedate):
    with open("lastdate.txt",'w') as f:
        #print 'writing to file: ' + time.strftime('%a %b %d %H:%M:%S +0000 %Y', thedate)
        f.write(time.strftime( '%a %b %d %H:%M:%S +0000 %Y', thedate))
        f.close()

def checkMoreRecent(datein):
    global maxDate
    if datein > maxDate:        
        maxDate = datein
    return datein > dateFromFile
    
def loadKnownFollowers():
    followers = []
    with open("followers.txt", 'r') as f:
        for line in f.readlines():
            followers.append(int(line))
        f.close()
    return followers
    
def writeKnownFollowers(known):
    with open("followers.txt",'w') as f:
        for k in known:
            f.write(str(k) + "\n")
        f.close()
    
def followback(t):
    # get the 20 newst followers
    current_followers = t.followers.ids()['ids']
    
    known = loadKnownFollowers()
    
    for c in current_followers:
        if c not in known:
            # Follow back
            print "Follow %d"%c
            known.append(c)
    writeKnownFollowers(known)
    
    
    

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
        CONSUMER_KEY, CONSUMER_SECRET))

dateFromFile = getDateFromFile()        

if len(sys.argv) > 1:
    if  sys.argv[1] == 'daily':        
        numba = int (random.random()*len(tweets))%len(tweets)
        #print tweets[numba]
        t.statuses.update(status=tweets[numba])
    elif sys.argv[1] == 'followback':
        followback(t)
else:
    for tweet in t.statuses.home_timeline():
        if  checkMoreRecent(parseDate(tweet['created_at'])) and  tweet['user']['screen_name'] != 'yolo_swag__420':
            #print tweet['user']['screen_name']
            #print tweet['text']
            thetime = parseDate(tweet['created_at'])
            for lamething in tweets:
                if (tweet['text'].find(lamething) != -1):
                    #print "@%s: %s!"%(tweet['user']['screen_name'], lamething)
                    t.statuses.update(status="%s %s"%(tweet['user']['screen_name'], lamething))
    
writeDateToFile(maxDate)

    

