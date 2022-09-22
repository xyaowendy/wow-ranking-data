#!/usr/bin/env python
#coding: utf-8
import requests
import warnings
import sys
warnings.filterwarnings("ignore")

dungeons = {}
## dungeon
dungeons['juchang'] = '%E4%BC%A4%E9%80%9D%E5%89%A7%E5%9C%BA'                             ## 伤势剧场
dungeons['diaohun'] = '%E5%87%8B%E9%AD%82%E4%B9%8B%E6%AE%87'                             ## 凋魂之殇
dungeons['xianlin'] = '%E5%A1%9E%E5%85%B9%E4%BB%99%E6%9E%97%E7%9A%84%E8%BF%B7%E9%9B%BE'  ## 仙林
dungeons['bijie'] = '%E5%BD%BC%E7%95%8C'                                                 ## 彼界
dungeons['gaota'] = '%E6%99%8B%E5%8D%87%E9%AB%98%E5%A1%94'                               ## 晋升高塔
dungeons['shuzui'] = '%E8%B5%8E%E7%BD%AA%E5%A4%A7%E5%8E%85'                              ## 赎罪大厅
dungeons['chihong'] = '%E8%B5%A4%E7%BA%A2%E6%B7%B1%E6%B8%8A'                             ## 赤红深渊
dungeons['tongling'] = '%E9%80%9A%E7%81%B5%E6%88%98%E6%BD%AE'                            ## 通灵站潮
dungeons['hongtu'] = '%E5%A1%94%E6%89%8E%E7%BB%B4%E4%BB%80%EF%BC%9A%E7%B4%A2%C2%B7%E8%8E%89%E4%BA%9A%E7%9A%84%E5%AE%8F%E5%9B%BE' ##宏图
dungeons['tianjie'] = '%E5%A1%94%E6%89%8E%E7%BB%B4%E4%BB%80%EF%BC%9A%E7%90%B3%E5%BD%A9%E5%A4%A9%E8%A1%97' ##天街
dungeons['kashang'] = '重返卡拉赞（上层）'
dungeons['kaxia'] = '重返卡拉赞（下层）'
dungeons['lajichang'] = '麦卡贡行动 - 垃圾场'
dungeons['chejian'] = '麦卡贡行动 - 车间'
dungeons['matou'] = '钢铁码头'
dungeons['chezhan'] = '恐轨车站'

realms = {}
## realm
realms['fenghuang'] = '%E5%87%A4%E5%87%B0%E4%B9%8B%E7%A5%9E'                           ## 凤凰之神                           
realms['kesjd'] = '%E5%85%8B%E5%B0%94%E8%8B%8F%E5%8A%A0%E5%BE%B7'  ##克尔苏加德
realms['bfg'] = '%E5%86%B0%E9%A3%8E%E5%B2%97'   ##冰风岗
realms['edsl'] = '%E5%9F%83%E5%BE%B7%E8%90%A8%E6%8B%89' ##埃德萨拉
realms['blkd'] = '%E5%B8%83%E5%85%B0%E5%8D%A1%E5%BE%B7' ##布兰卡德
realms['yzas'] = '%E5%BD%B1%E4%B9%8B%E5%93%80%E4%BC%A4'  ##影之哀伤
realms['wjzh'] = '%E6%97%A0%E5%B0%BD%E4%B9%8B%E6%B5%B7' ##无尽之海
realms['pjzd'] = '%E8%B4%AB%E7%98%A0%E4%B9%8B%E5%9C%B0'  ##贫瘠之地
realms['gwzg'] = '%E5%9B%BD%E7%8E%8B%E4%B9%8B%E8%B0%B7'  ##国王之谷
realms['ge'] = '%E6%A0%BC%E7%91%9E%E5%A7%86%E5%B7%B4%E6%89%98'                         ## 格瑞姆巴托
realms['ranshao'] = '%E7%87%83%E7%83%A7%E4%B9%8B%E5%88%83'                              ## 燃烧之刃
realms['siwang'] = '%E6%AD%BB%E4%BA%A1%E4%B9%8B%E7%BF%BC'                              ## 死亡之翼
realms['yiseng'] = '%E4%BC%8A%E6%A3%AE%E5%88%A9%E6%81%A9'                              ## 伊森利恩
realms['ansu'] = '%E5%AE%89%E8%8B%8F'                                ## 安苏
realms['xuese'] = '%E8%A1%80%E8%89%B2%E5%8D%81%E5%AD%97%E5%86%9B'                               ## 血色十字军
realms['baiyin'] = '%E7%99%BD%E9%93%B6%E4%B9%8B%E6%89%8B'   #白银之手
realms['luoning'] = '%E7%BD%97%E5%AE%81' #罗宁
realms['zhuzhai'] = '%E4%B8%BB%E5%AE%B0%E4%B9%8B%E5%89%91'    #主宰之剑
realms['xiongmao'] = '%E7%86%8A%E7%8C%AB%E9%85%92%E4%BB%99'  #熊猫酒仙
realms['jinse'] = '%E9%87%91%E8%89%B2%E5%B9%B3%E5%8E%9F'  #金色平原

def track(dungeon, realm, periodId, page):
    baseurl = 'https://tavern.blizzard.cn/action/api/common/v3/wow/mythic-dungeon/rank?'
    baseurl += 'dungeon='+ dungeons[dungeon] + '&periodId=' + periodId + '&realm=' + realms[realm] + '&p='
    header = {'Host': 'tavern.blizzard.cn',
              'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.21(0x17001520) NetType/WIFI Language/zh_CN',
              'Referer': 'https://servicewechat.com/wx02935bb29080a7b4/159/page-frame.html'}
    res = requests.get(baseurl+str(page), headers=header, verify=False)
    res.encoding = 'utf8'
    print(res.text)


if __name__ == "__main__":
    usage = "Track Mythic Dungeon.\n" + \
            "  Usage: python3 {} Dungeon, Realm, PeriodId, Page ".format(sys.argv[0])
    if len(sys.argv) != 5:
        print(usage)
        sys.exit(-1)
    track(sys.argv[1], sys.argv[2], str(sys.argv[3]), sys.argv[4])
