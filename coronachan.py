import json
import os
import sys
import urllib.parse
import urllib3


def handler(event, context):
    return {
        'message': coronachan()
    }


def coronachan():
    token = os.environ['TOKEN'] 
    cookie = os.environ['COOKIE'] 
    slack = os.environ['SLACK'] 
    http = urllib3.PoolManager()

    r = http.request('GET', 'https://api.coronatracker.com/v3/stats/worldometer/country?countryCode=MY')
    if r.status != 200 or len(json.loads(r.data.decode('utf-8'))) != 1:
        return("Error getting corona data")
    coronaData = json.loads(r.data.decode('utf-8'))
    total = coronaData[0]["totalConfirmed"] + 1
    p = http.request('GET', 'https://slack.com/api/users.profile.get?token=' + token + '&pretty=1', headers={"cookie": cookie})
    profile = json.loads(p.data.decode('utf-8'))
    if r.status != 200 or profile["ok"] == False:
        return("Error getting corona data")
    title = profile["profile"]["title"]
    current = int("".join(filter(str.isdigit, title)))
    if total > current:
        # update
        newProfile = {"title": "编号#" +
                        str(total), "status_text": "编号#" + str(total), }
        queryObj = {'token': token,
                    'profile': str(newProfile),
                    'pretty': 1}
        qs = urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote)
        u = http.request('POST', 'https://slack.com/api/users.profile.set?' + qs, headers={"cookie": cookie})
        if u.status != 200:
            return("Error updating profile")
        # slack notification
        slackObj = {"text": "BB is now 编号#" + str(total)}
        jsonStr = json.dumps(slackObj)
        s = http.request('POST', slack, body=jsonStr)
        if s.status != 200:
            return("Error sending slack notification")
    return("Slack status up to date")
