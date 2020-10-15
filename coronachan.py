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
queryObj = {'tweet_mode': "extended"}
qs = urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote)

def handler(event, context):
    return {
        'message': coronachan()
    }

def infographic():
    queryObj = {'tweet_mode': "extended"}
    qs = urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote)
    t = http.request('GET', 'https://api.twitter.com/2/timeline/profile/1124170610920189952.json?' +
                qs, headers={"cookie": twitterCookie, "authorization": twitterToken, "host": "api.twitter.com", "x-csrf-token": "cdad10dbdd00df5a29bd886eebe4653a"})
    tweet = json.loads(t.data.decode('utf-8'))
    if t.status != 200:
        print("Error getting corona data")
    tweets = tweet["globalObjects"]["tweets"]

    for tweet in tweets:
        if 'PERINCIAN KES SETIAP NEGERI - ' + date.today().strftime("%d").strip("0") in tweets[tweet]["full_text"] and tweets[tweet]["full_text"].startswith('RT') == False:
            pic = tweets[tweet]["entities"]["media"][0]["media_url"]
            txt = 'PERINCIAN KES SETIAP NEGERI' + tweets[tweet]["full_text"].partition(
             "PERINCIAN KES SETIAP NEGERI")[2].partition("https")[0]
            slackObj = {"text": txt,
                    "blocks": [
                        {
                            "type": "section",
                            "block_id": "section567",
                            "text": {
                                "type": "mrkdwn",
                                "text": txt
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": pic,
                                "alt_text": "coronachan status"
                            }
                        }
                    ]              
                }
            jsonStr = json.dumps(slackObj)
            s = http.request('POST', slack, body=jsonStr)
        if 'PERINCIAN KES NEGERI SELANGOR - ' + date.today().strftime("%d").strip("0") in tweets[tweet]["full_text"] and tweets[tweet]["full_text"].startswith('RT') == False:
            pic = tweets[tweet]["entities"]["media"][0]["media_url"]
            txt = 'PERINCIAN KES NEGERI SELANGOR' + tweets[tweet]["full_text"].partition(
             "PERINCIAN KES NEGERI SELANGOR")[2].partition("https")[0]
            slackObj = {"text": txt,
                    "blocks": [
                        {
                            "type": "section",
                            "block_id": "section567",
                            "text": {
                                "type": "mrkdwn",
                                "text": txt
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": pic,
                                "alt_text": "coronachan status"
                            }
                        }
                    ]              
                }
            jsonStr = json.dumps(slackObj)
            s = http.request('POST', slack, body=jsonStr)
    


def coronachan():
    queryObj = {'tweet_mode': "extended"}
    qs = urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote)
    t = http.request('GET', 'https://api.twitter.com/2/timeline/profile/531041640.json?' +
                    qs, headers={"cookie": twitterCookie, "authorization": twitterToken, "host": "api.twitter.com", "x-csrf-token": "cdad10dbdd00df5a29bd886eebe4653a"})
    tweet = json.loads(t.data.decode('utf-8'))
    if t.status != 200:
        return("Error getting corona data")
    tweets = tweet["globalObjects"]["tweets"]
    for tweet in tweets:
        if tweets[tweet]["full_text"].startswith('Terkini #COVID19Malaysia ' + date.today().strftime("%d").strip("0")):

            totalStr = tweets[tweet]["full_text"].partition(
                "Jumlah positif= ")[2].partition("Kes kematian=")[0]
            total =  int("".join(filter(str.isdigit, totalStr))) + 1
            newStr =  tweets[tweet]["full_text"].partition(
                "Kes positif= ")[2].partition("kes import")[0]
            new = int("".join(filter(str.isdigit, newStr)))
            deathStr = tweets[tweet]["full_text"].partition(
                "Kes kematian=")[2].partition("Jumlah kes kematian")[0]
            death = int("".join(filter(str.isdigit, deathStr)))
            totalDeathStr = tweets[tweet]["full_text"].partition(
                "Jumlah kes kematian= ")[2].partition("Kes dirawat di ICU")[0]
            totalDeath = int("".join(filter(str.isdigit, totalDeathStr)))
            totalRecoveredStr =  tweets[tweet]["full_text"].partition(
                "Jumlah kes sembuh= ")[2].partition("Kes positif")[0]
            totalRecovered = int("".join(filter(str.isdigit, totalRecoveredStr)))
            recoveredStr =  tweets[tweet]["full_text"].partition(
                "Kes sembuh=")[2].partition("Jumlah kes sembuh")[0]
            recovered = int("".join(filter(str.isdigit, recoveredStr)))
            active = total - totalRecovered - totalDeath
            pic = tweets[tweet]["entities"]["media"][0]["media_url"]
    p = http.request('GET', 'https://slack.com/api/users.profile.get?token=' + slackToken + '&pretty=1', headers={"cookie": slackCookie})
    profile = json.loads(p.data.decode('utf-8'))
    if p.status != 200 or profile["ok"] == False:
        return("Error getting current slack status")
    title = profile["profile"]["title"]
    current = int("".join(filter(str.isdigit, title)))
    if total <= current:
            return("Slack status up to date")
    # update
    newProfile = {"title": "编号#" +
                    str(total), "status_text": "编号#" + str(total), }
    queryObj = {'token': slackToken,
                'profile': str(newProfile),
                'pretty': 1}
    qs = urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote)
    u = http.request('POST', 'https://slack.com/api/users.profile.set?' + qs, headers={"cookie": slackCookie})
    if u.status != 200:
        infographic()
        return("Error updating profile")
    # slack notification
    slackObj = {"text": "BB is now 编号#" + str(total),
                "blocks": [
                    {
                        "type": "section",
                        "block_id": "section567",
                        "text": {
                            "type": "mrkdwn",
                            "text": "BB is now 编号#" + str(total) + "\n Total Confirmed: " + str(total - 1) + " (+" + str(new) + ") \n Total Death: " + str(totalDeath) + " (+" + str(death) + ") \n Total Recovered: " + str(totalRecovered) + " (+" + str(recovered) + ") \n Total Active: " + str(active)
                        },
                        "accessory": {
                            "type": "image",
                            "image_url": pic,
                            "alt_text": "coronachan status"
                        }
                    }
                ]              
            }
    jsonStr = json.dumps(slackObj)
    s = http.request('POST', slack, body=jsonStr)
    if s.status != 200:
        infographic()
        return("Error sending slack notification")
    infographic()
    return('Updated slack status')
    