import json
import os
import requests
import sys
import urllib.parse

token = os.environ['TOKEN'] 
cookie = os.environ['COOKIE'] 
slack = os.environ['SLACK'] 

resp = requests.get(
    'https://api.coronatracker.com/v3/stats/worldometer/country?countryCode=MY')
total = resp.json()[0]["totalConfirmed"] + 1
profile = requests.get(
    'https://slack.com/api/users.profile.get?token=' + token + '&pretty=1', headers={"cookie": cookie})
if profile.json()["ok"] == False:
    sys.exit("Error getting profile!")
title = profile.json()["profile"]["title"]
status = profile.json()["profile"]["status_text"]
current = int("".join(filter(str.isdigit, title)))
if total > current:
    # update
    newProfile = {"title": "编号" +
              str(total), "status_text": "编号#" + str(total), }
    queryObj = {'token': token,
                    'profile': str(newProfile),
                    'pretty': 1}
    qs = urllib.parse.urlencode(queryObj, quote_via=urllib.parse.quote)
    update = requests.post('https://slack.com/api/users.profile.set?' + qs, headers={"cookie": cookie})
    if update.status_code != 200 or update.json()["ok"] == False:
        sys.exit("Error updating profile!")
    #slack notification
    slackObj = {"text": "BB is now 编号#"+ str(total)}
    jsonStr = json.dumps(slackObj)
    slack = requests.post(slack, data = jsonStr)
    print("Updated slack status")
    exit()
print("Slack status up to date")