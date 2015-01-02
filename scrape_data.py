__author__ = 'kjoseph'

import requests
from time import sleep
import simplejson as json
from pymongo import MongoClient
from my_utils import print_json

[USER, API_KEY] = [l.strip() for l in open("../key_info.txt").readlines()]
print USER, API_KEY

API = "http://api.nytimes.com/svc/politics/v3/us/legislative/"
params = {"api-key": API_KEY}

def get_members(db_senate_members, congress_num, from_api=True):
    ##from_api is a shortcut... wanted to show how we got the data
    ##originally but once its in the db we just want to load from there
    output = []
    if not from_api:
        return [obj['_id'] for obj in db.senate_members.find()]

    url_to_hit = API + "congress/"+str(congress_num)+"/senate/members.json"
    response = requests.get(url_to_hit,params=params).json()
    senate_member_json = response['results'][0]
    congress_num = senate_member_json['congress']
    chamber = senate_member_json['chamber']
    for member in senate_member_json['members']:
        print member['id']
        member['nyt_id'] = member['id']
        del member['id']
        member['congress_number'] = congress_num
        member['chamber'] = chamber
        output.append(db_senate_members.insert(member))
    return [o for o in output if o is not None]

def get_bill(bill_id, bills_db,congress_num):
    output = []

    url_to_hit = API + "congress/" + str(congress_num) + "/bills/"+ bill_id+"/cosponsors.json"
    print url_to_hit
    sleep(3)
    response = requests.get(url_to_hit,params=params)
    print response
    response_json = response.json()['results'][0]
    print json.dumps(response_json)
    return bills_db.insert(response_json)


client = MongoClient()
db = client['senate_voting_records']

bill_ids = ['s'+str(bill_id) for bill_id in range(599,2370)]

for congress in [113]:
    members = get_members(db.senate_members,congress)
    bills = []
    for bill_id in bill_ids:
        print 'starting collection for: ', bill_id
        bills.append(get_bill(bill_id, db.bills,congress))
