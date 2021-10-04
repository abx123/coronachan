import json
import os
import sys
import urllib.parse
import urllib3
from datetime import date

twitterToken = os.environ['TWITTERTOKEN']  
twitterCookie = os.environ['TWITTERCOOKIE']
slackToken = os.environ['SLACKTOKEN'] 
slackCookie = os.environ['SLACKCOOKIE']
slack = os.environ['SLACK']
http = urllib3.PoolManager()

def sendSlackMsg(json):
    s = http.request('POST', slack, body=json)
    if s.status != 200:
        raise Exception("Error sending slack notification")
    print('Slack message sent')

def crawlKKM():
    month = {
        1: "Januari",
        2: "Febuari",
        3: "Mac",
        4: "April",
        5: "Mei",
        6: "Jun",
        7: "Julai",
        8: "Ogos",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Disember",
    }
    total = '0'
    queryObj = {'tweet_mode': "extended", 'count': 20}
    qs = urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote)
    t = http.request('GET', 'https://api.twitter.com/2/timeline/profile/1595149746.json?' +
                    qs, headers={"cookie": twitterCookie, "authorization": twitterToken, "host": "api.twitter.com", "x-csrf-token": "58a90ffef07c544d2c6fc83f649174ba8897a334b927e60d539e8e6f203defdc2a4da1e93fc80ff96adf10f9c298f72390227acf1e1f2e1716cdbc96892b0b95191e65dfafc2a3b8ea7a7808a99d4780"})
    
    if t.status != 200:
        raise Exception("Error getting corona data")
    tweet = json.loads(t.data.decode('utf-8'))
    tweets = tweet["globalObjects"]["tweets"]

    for tweet in tweets:
        if ((date.today().strftime("%#d") + ' ' +  month[int(date.today().strftime("%#m"))] in tweets[tweet]["full_text"]  and 'Sehingga' and 'Jumlah kes COVID-19'in tweets[tweet]["full_text"])):
            newStr = tweets[tweet]["full_text"].split("dilaporkan adalah")[1].split(".")[0].split("(")[0]
            totalStr = tweets[tweet]["full_text"].split("dilaporkan adalah")[1].split(".")[0].split("(")[1]
            
            new = int("".join(filter(str.isdigit, newStr)))
            total = int("".join(filter(str.isdigit, totalStr)))
            
            slackStatus = getSlackStatus()
            current = int("".join(filter(str.isdigit, slackStatus)))
            if total <= current:
                return("Slack status up to date")
            
            newProfile = {"title": "编号#" +
                    str(total+1), "status_text": "编号#" + str(total+1), "status_emoji": ":bb-dieded:",}
            queryObj = {'token': slackToken,
                        'profile': str(newProfile),
                        'pretty': 1}
            setSlackStatus(urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote))
            slackObj = {"text": "KiteFishBB is now 编号#" + str(total+1),
                "blocks": [
                    {
                        "type": "section",
                        "block_id": "section567",
                        "text": {
                            "type": "mrkdwn",
                            "text": "KiteFishBB is now 编号#" + str(total+1) + "\n Total Confirmed: " + str(total) + " (" + str(new) + ")" 
                        }
                    }
                ]              
            }
            sendSlackMsg(json.dumps(slackObj))

def getSlackStatus():
    p = http.request('GET', 'https://slack.com/api/users.profile.get?token=' + slackToken + '&pretty=1', headers={"cookie": slackCookie})
    profile = json.loads(p.data.decode('utf-8'))
    if p.status != 200 or profile["ok"] == False:
        raise Exception("Error getting current slack status")
    return profile["profile"]["title"]

def setSlackStatus(qs):
    u = http.request('POST', 'https://slack.com/api/users.profile.set?' + qs, headers={"cookie": slackCookie})
    if u.status != 200:
        raise Exception("Error updating profile")

def handler(event, context):
    kkm = crawlKKM()
    if kkm is None:
        kkm = ''
    return {
        'message': kkm 
    }
