__author__ = 'kjoseph'


#%%

import glob, itertools, sys, os
import simplejson as json
from collections import Counter
import yaml
import cPickle as pickle

###DATA FROM: https://github.com/unitedstates/congress
DATA_DIRECTORY = os.path.join("/Users/kjoseph/git/congress_voting/","data")

def get_votes_network():
    network = Counter()

    senator_set = set()
    for fil in glob.iglob(DATA_DIRECTORY+"/votes/*/s*/data.json"):

        with open(fil) as file:
            data = json.load(file)

            ##if its not a bill, or its not the senate
            ##or there were no `Yea' votes, continue
            if 'bill' not in data or\
                data['bill']['type'] != 's' or\
                'votes' not in data or\
                'Yea' not in data['votes']:
                continue

            all_yea_voters = set([voter['id'] for voter in data['votes']['Yea']])
            for x in all_yea_voters:
                senator_set.add(x)

            for i in itertools.combinations(all_yea_voters,2):
                if i[0] < i[1]:
                    network[i[0],i[1]] +=1
                else:
                    network[i[1],i[0]] +=1
    return senator_set, network

def get_bill_network():
    network = Counter()

    senator_set = set()
    for fil in glob.iglob(DATA_DIRECTORY + "/bills/s/s*/data.json"):

        ##if bill in json and type in json['bill'] and type == 's'
            #go get bill,
        with open(fil) as file:
            data = json.load(file)
            all_sponsors = set([cosponsor['thomas_id'] for cosponsor in data['cosponsors']])
            all_sponsors.add(data['sponsor']['thomas_id'])
            for x in all_sponsors:
                senator_set.add(x)

            for i in itertools.combinations(all_sponsors,2):
                if int(i[0]) < int(i[1]):
                    network[i[0],i[1]] +=1
                else:
                    network[i[1],i[0]] +=1
    return senator_set, network

def get_senator_data(thomas_id_set, lis_id_set):

    senator_thomas_data = dict()
    senator_lis_data = dict()
    with open(os.path.join(DATA_DIRECTORY,"legislators-current.yaml")) as file:
        all_data = yaml.load(file)
        for x in all_data:
            if 'thomas' in x['id'] and x['id']['thomas'] in thomas_id_set:
                senator_thomas_data[x['id']['thomas']] = x
                if 'lis' not in x['id']: print 'WTF no lis'

            if 'lis' in x['id'] and x['id']['lis'] in lis_id_set:
                senator_lis_data[x['id']['lis']] = x
                if 'thomas' not in x['id']: print 'WTF no thomas'

    with open(os.path.join(DATA_DIRECTORY,"legislators-historical.yaml")) as file:
        all_data = yaml.load(file)
        for x in all_data:
            if 'thomas' in x['id'] and x['id']['thomas'] in thomas_id_set:
                senator_thomas_data[x['id']['thomas']] = x

            if 'lis' in x['id'] and x['id']['lis'] in lis_id_set:
                senator_lis_data[x['id']['lis']] = x
    return senator_thomas_data, senator_lis_data


def print_network(network, filename):
    out_fil_l = open("/Users/kjoseph/Dropbox/Public/"+filename+".csv","w")
    out_fil_l.write("name1\tname2\tweight\n")
    for l in network:
        out_fil_l.write(senators[l['source']] + "\t" + senators[l['target']] + "\t" + str(l['value']) + "\n")
    out_fil_l.close()
#%%

lis_id_set, vote_network = get_votes_network()
thomas_id_set, bill_network = get_bill_network()
senator_thomas_data, senator_lis_data = get_senator_data(thomas_id_set, lis_id_set)
#%%

output_data = {}
thomas_index_dict = {}
lis_index_dict = {}
node_index = 0
senators = []

output_data['nodes'] = []
for k, senator in senator_thomas_data.iteritems():
    group_val = 0
    if senator['terms'][-1]['party'] == 'Democrat':
        group_val = 1
    if senator['terms'][-1]['party'] == 'Republican':
        group_val = 2
    
    output_data['nodes'].append({ "name": senator['name']['official_full'],
                                  "group": senator['terms'][-1]['party'] })
    thomas_index_dict[senator['id']['thomas']] = node_index
    lis_index_dict[senator['id']['lis']] = node_index
    senators.append(senator['name']['official_full'])
    node_index += 1


bill_links = []
for x,v in bill_network.iteritems():
    if x[0] not in thomas_index_dict or x[1] not in thomas_index_dict:
        print 'WTF', x, v
    else:
        bill_links.append({ "source":thomas_index_dict[x[0]], "target":thomas_index_dict[x[1]],"value":v})
output_data['bill_network'] = bill_links

vote_links = []
for x,v in vote_network.iteritems():
    if x[0] not in lis_index_dict or x[1] not in lis_index_dict:
        print 'WTF', x, v
    else:
        bill_links.append({ "source":lis_index_dict[x[0]], "target":lis_index_dict[x[1]],"value":v})
output_data['vote_network'] = bill_links

out_fil_n = open("/Users/kjoseph/Dropbox/Public/nodes.csv","w")
out_fil_n.write("name\tgroup\n")
for n in output_data['nodes']:
    out_fil_n.write(n['name'] + "\t" + n['group'] + "\n")
out_fil_n.close()

print_network(output_data['vote_network'],"vote_network")
print_network(output_data['bill_network'],"bill_network")
