#!/usr/bin/env python3
#coding: utf-8

import json
import copy
import time as timer
from pymongo import MongoClient
import certifi

import matplotlib.pyplot as plt
from matplotlib import font_manager
font = font_manager.FontProperties(fname='microsoft_yahei.ttc')

time = {'塔扎维什：琳彩天街':39,
        '塔扎维什：索·莉亚的宏图':30,
        '恐轨车站':30,
        '钢铁码头':30,
        '麦卡贡行动 - 垃圾场':38,
        '麦卡贡行动 - 车间':32,
        '重返卡拉赞（上层）':35,
        '重返卡拉赞（下层）':42,
        }

classid = {'1':'战士', '2':'骑士', '3':'猎人', '4':'盗贼', 
           '5':'牧师', '6':'死亡骑士', '7':'萨满', '8':'法师', 
           '9':'术士', '10':'武僧', '11':'德鲁伊', '12':'恶魔猎手',
           'null':'null'}

def calculate_score(level, t, d):
    limit_time = float(time[d])
    remain = limit_time - t
    if remain > -0.016777:
        ex = min(7.5, remain * 7.5 / (0.4 * limit_time))
        score = 75 + level * 7.5 + ex
        flag = ""
    else:
        if remain < -0.4 * limit_time:
           score = 0
        else:
           ex = min(-7.5, remain * 15 / (0.4 * limit_time))
           score = 75 + level * 7.5 + ex
        flag = '-'
    return score, flag



def read_js(fn_lst):
    datas = []
    print('reading json file')
    with open(fn_lst, 'r') as f:
        for fn in f.readlines():
            with open(fn.strip(), 'r') as f:
                datas.append(json.load(f)['data'])
                if len(datas) % 10000 == 0:
                   print('{}: read {} json file'.format(timer.asctime() ,len(datas)))
    return datas

def parse_js(datas):
    '''
    A json instance
    { 
      affixes:
      dungeon:
      p:
      pTotal:
      periodId
      teams: [
        dungeon:{}
        duration: 1780766
        faction: ALLIANCE
        keystoneLevel: 28
        members: [ 
                 classId: 4
                 id: IuCZiqfvumxibC1ayAQImtcTCdmxviGdpJSiroyfVtA
                 name: 山***山
                 realm: 国王之谷
                 role: HEALER
                 specializationId: 257
                 ]
              ]           
     }
    '''
    print("parse json")
    recs = {}
    users = {}
    for data in datas:
        dungeon = data['dungeon']
        periodId = data['periodId']
        index = int(periodId) % 2
        init_logs = {}
        for key in time:
            # init_logs[key] = [[[0, 247.5, 23, -1, '']],[[1, 247.5, 23, -1, '']]]
            init_logs[key] = [[[0, 0, 0, -1, '']],[[1, 0, 0, -1, '']]]
        for team in data['teams']:
            duration = float(team['duration']) / 60 / 1000
            level = team['keystoneLevel']
            members = team['members']
            score, flag = calculate_score(level, duration, dungeon)
            for member in members:
                cid = str(member['classId'])
                uid = member['id']
                name = member['name']
                realm = member['realm']
                log = [periodId, score, level, duration, flag]
                if uid not in users:
                   users[uid] = [name, realm, classid[cid]]
                   recs[uid] = copy.deepcopy(init_logs)
                   recs[uid][dungeon][index].append(log)
                else:
                   if log not in recs[uid][dungeon][index]:
                      recs[uid][dungeon][index].append(log)
    return recs, users
     
def merge(recs, users):
    print('merge ...')
    merge_keys = {}
    merge_recs = {}
    free_keys = ['小***了-法师','月*-法师']
    same_keys = {
                 'Nep****e-牧师':'烤***了-牧师', 
                 '中***奶-牧师':'田**饱-牧师',
                 '藏****梦-死亡骑士':'淸****生-死亡骑士',
                 '芭**雅-牧师':'阿**特-牧师', 
                 'Sem**ê-法师':'Sem**e-法师',
                 '遵***丶-术士':'遵**王-术士', 
                 'Fra*****k-死亡骑士':'萌****啦-死亡骑士', 
                 '术**宝-术士':'Vme***e-术士', 
                 '美****寳-法师':'另*-法师'
                }
    inum = 0
    for uid in users:
        user = users[uid]
        key  = user[0] + '-' + user[2]
        if key in free_keys:
           key = key + str(inum) 
           inum += 1
        if key in same_keys:
           key = same_keys[key]
           print(key)
        if key not in merge_keys:
           merge_keys[key] = [uid]
        else:
           merge_keys[key].append(uid)
    for key in merge_keys:
        uids = merge_keys[key]
        merge_recs[uids[-1]] = recs[uids[-1]]
        if len(uids) > 1:
           for dungeon in time:
               for uid in uids[:-1]:
                   for log in recs[uid][dungeon][0]:
                       merge_recs[uids[-1]][dungeon][0].append(log)
                   for log in recs[uid][dungeon][1]:
                       merge_recs[uids[-1]][dungeon][1].append(log)
    return merge_recs
           
def get_rank(recs, users):
    print('ranking ...')
    ranks = []
    for uid in recs:
        key = users[uid][0] + '-' + users[uid][1]
        pclass = users[uid][2]
        score = 0
        info = ''
        for dungeon in time:
            log0 = sorted(recs[uid][dungeon][0], key=lambda x:x[1])[-1]
            log1 = sorted(recs[uid][dungeon][1], key=lambda x:x[1])[-1]
            info += str(log0[2]) + log0[-1] + ' / ' + str(log1[2]) + log1[-1] + '\t'
            score +=  max(log0[1], log1[1]) + 0.33333 * min(log0[1], log1[1])
        ranks.append([key, pclass, info, score])
    ranks.sort(reverse=True, key=lambda x:x[-1])
    return ranks

def upload(recs, users):
    print('uploading ...')
    datas = []
    for uid in recs:
        key = users[uid][0] + '-' + users[uid][1]
        pclass = users[uid][2]
        score = 0
        data = {}
        data['ID'] = key
        data['职业'] = pclass
        for dungeon in time:
            log0 = sorted(recs[uid][dungeon][0], key=lambda x:x[1])[-1]
            log1 = sorted(recs[uid][dungeon][1], key=lambda x:x[1])[-1]
            score +=  max(log0[1], log1[1]) + 0.33333 * min(log0[1], log1[1])
            data[dungeon] = str(log0[2]) + log0[-1] + ' / ' + str(log1[2]) + log1[-1]
        data['总分'] = (score)
        datas.append(data)
    datas.sort(reverse=True, key=lambda x:x['总分'])
    # datas = json.dumps(datas, ensure_ascii = False, indent=4, separators=(',', ':'))
    # print(datas)
    ca = certifi.where()
    client = MongoClient("mongodb+srv://admin:oo4KBdt7tSjF2ADr@mycluster.mbzbjc0.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
    db = client.wowdb
    collection = db["Players"]
    collection.drop()
    collection.insert_many(datas[:5000])
    

def plot(ranks):
    counts = {'战士':0, '骑士':0, '猎人':0, '盗贼':0, 
               '牧师':0, '死亡骑士':0, '萨满':0, '法师':0, 
               '术士':0, '武僧':0, '德鲁伊':0, '恶魔猎手':0}
    colors = {'战士':'#C69B6D', '骑士':'#F48CBA', '猎人':'#AAD372', '盗贼':'#FFF468', 
               '牧师':'#F0EBE0', '死亡骑士':'#C41E3B', '萨满':'#2359FF', '法师':'#68CCEF', 
               '术士':'#9382C9', '武僧':'#00FE95', '德鲁伊':'#FF7C0A', '恶魔猎手':'#A22FC8'}
    color = []
    for rank in ranks:
        counts[rank[1]] += 1
    counts = dict(sorted(counts.items(), key=lambda x:x[1], reverse = True))
    for cid in counts:
        color.append(colors[cid])
    bar = plt.bar(list(counts.keys()), counts.values(), color=color)
    for data in bar:
        y = data.get_height()
        x = data.get_x()
        plt.text(x + 0.12, y, str(y), va='bottom', fontsize = 8)
    index = range(len(counts))
    plt.xticks(index, [], fontproperties = font, fontsize = 8)
    
    plt.savefig('./1.jpg')
    plt.close()

if __name__ == "__main__":
    js_fn_lst = 'data.lst'
    datas = read_js(js_fn_lst)
    recs, users = parse_js(datas)
    merge_recs = merge(recs, users)
    upload(recs, users)
    # ranks = get_rank(merge_recs, users)
    # plot(ranks[:1000])
    # out_f = open('./out', 'w')
    # for rank in ranks:
    #     out_f.write('{}\t{}\t{}{}\n'.format(rank[0], rank[1], rank[2], rank[3]))
