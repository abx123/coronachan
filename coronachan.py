import json
import os
import sys
import urllib.parse
import urllib3
from datetime import date

twitterToken = os.environ['TWITTERTOKEN']  =  "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
twitterCookie = os.environ['TWITTERCOOKIE']  = '_ga=GA1.2.1015214462.1496167800; syndication_guest_id=v1%3A155404109367761835; __utma=43838368.1015214462.1496167800.1553831103.1560884178.6; kdt=stshoXCg0JpQ7ijSvCS6RaavEKhqBG1uptXItMIY; lang=en; _gid=GA1.2.1047439290.1607514808; at_check=true; des_opt_in=Y; _sl=1; gt=1337143682512785408; remember_checked_on=1; mbox=PC#abbef2290b904620b49d7785105794b9.38_0#1670879950|session#1fefa80402a640fe9a3b1b2a0c0a8d51#1607636401; ads_prefs="HBERAAA="; auth_multi="1291129677910687744:0dde3649ad11742e32699de5d05afe3cb5b020b4"; auth_token=64b0998ad4662b113066377046fa75ad4a049aa7; twid=u%3D1337142978398195713; ct0=58a90ffef07c544d2c6fc83f649174ba8897a334b927e60d539e8e6f203defdc2a4da1e93fc80ff96adf10f9c298f72390227acf1e1f2e1716cdbc96892b0b95191e65dfafc2a3b8ea7a7808a99d4780; personalization_id="v1_b0/oZDtKOg7jyAgVPtkw4g=="; guest_id=v1%3A160763533999372561'
slackToken = os.environ['SLACKTOKEN']   = "xoxc-1217388489398-1224329303043-1274841758659-b6eb9111add29993339d5cf48e5a529bc7730b37bfeee9d3ae04b784edfd08a5"
slackCookie = os.environ['SLACKCOOKIE']  = "b=.6chv0pjfdzeksjzoktytkddgo; __qca=P0-445988570-1566412746466;_ga=GA1.2.1471926068.1566412746;optimizelyEndUserId=oeu1586404162521r0.5527341268071382;_gcl_au=1.1.1582809715.1594032219; _fbp=fb.1.1594032237823.1858811933;visitor_id755253=388703313;visitor_id755253-hash=2d47cb859182593f11e605a7032232af90073cb5885f934196159e1c532703b48bc005c4da48af5bb5210053d1f9f626f8ca40bf;d=%2B8tXAHr2Y%2FuRxf8lHQT1qh41F3KpVqrUA8Us9Hauk%2F0Dpu2ZGcaC1fsXbtauNanHXLMF0k4vD2kDGh0W7xQn179bJXifDdLwTCejh0YoMzt9QHXqsRgSbGCOpaG9sN2wXYem1YurjFFYm2kwGBA9zfCcGNI7xBybaQUsiL7hHPynQB32Zdp7MNL69A%3D%3D;driftt_aid=5f2833d4-84a1-4068-8d8c-711a9da03ba9;DFTT_END_USER_PREV_BOOTSTRAPPED=true;utm=%7B%22utm_source%22%3A%22in-prod%22%2C%22utm_medium%22%3A%22inprod-customize_link-slack_me%22%7D;d-s=1599735166; _gid=GA1.2.251723347.1599735170;x=6chv0pjfdzeksjzoktytkddgo.1599737216; DriftPlaybook=A;_lc2_fpi=e00b11ac9c9b--01ehvwbfqwyzd4czv4xs7c4vny;driftt_sid=c2154bb8-0a81-4f83-a47e-78cc5f950600;_uetsid=0c3fc851b99b08b83ffab76996a50064;_uetvid=372cab24f101372f975bc57deb8f5726"
slack = os.environ['SLACK']  = "https://hooks.slack.com/services/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"
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
        if ((date.today().strftime("%#d") + ' ' +  month[int(date.today().strftime("%#m"))] in tweets[tweet]["full_text"]  and 'Sehinga' and 'Jumlah kes COVID-19'in tweets[tweet]["full_text"])):
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
