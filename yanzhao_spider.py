import json
import requests
import pandas as pd
import os
import datetime
import numpy as np
 
def find_school(page, search, headers):
    if page == 0:
        data={
        'pageSize': 20,
        'start': '',
        'orderBy':'' ,
        'mhcx': 1,
        'ssdm2': '',
        'xxfs2': '',
        'dwmc2': '大学',
        'data_type': 'json',
        'agent_from':'wap',
        'pageid': ''
        }
    else:
        data={
        'pageSize': 20,
        'start': page*20,
        'orderBy':'' ,
        'mhcx': 1,
        'ssdm2': '',
        'xxfs2': '',
        'dwmc2': search,
        'data_type': 'json',
        'agent_from':'wap',
        'pageid': 'tj_qe_list'
        }
    try:
        url = "https://yz.chsi.com.cn/sytj/stu/sytjqexxcx.action"
        r=requests.post(url,headers=headers,timeout=30,data=data)
        r.raise_for_status()
        r.encoding='utf-8'
        text=json.loads(r.text)
        content=text['data']['vo_list']['vos']
        return content
    except:
        pass

def parse_one_page(content):
    type_dict = {}
    type_dict['1'] = "全日制"
    type_dict['2'] = "非全日制"
    for item in content:
        yield{
            'school': item['dwmc'],
            'academic': item['yxsmc'],  # 院系所
            'major': item['zymc'], # 专业
            'majorID': item['zydm'], 
            'schoolID': item['dwdm'],
            'direction':item['yjfxmc'], # 研究方向
            'type':type_dict[str(item['xxfs'])], # 1:全日制 2:非全日制
            'remain':item['qers'], #计划余额（人数）0表示有
            'publish':item['gxsj'], # 已发布多久
            'fit':item['sfmzjybyq'], # 是否符合调剂要求
            'conditions':"".join(item['bz'].split()), # 申请条件
            'test_requirement':item['sfmzyq'] # 无法申请的原因
            
        }

def data_processing(path):
    df = pd.read_csv(path,error_bad_lines=False)
    df.columns = ['招生单位','院系所','专业','研究方向','学习方式','计划余额','最后更新','符合调剂','初试要求','申请条件及信息']
    df.drop(df[(df['符合调剂'] == '不符合调入专业学科门类要求')|(df['符合调剂'] == '不符合调入专业初试科目要求')].index,inplace=True)
    # df.drop(df[df['初试要求'] != ""].index,inplace=True)
    df.drop(df[pd.isnull(df['初试要求'])==False].index,inplace=True)
    df.drop(['符合调剂','初试要求'],axis=1,inplace=True)
    # print(arr[pd.isnull(arr['numTest'])==True])
    df['计划余额'] = df['计划余额'].apply(lambda x:'有' if x==0 else x)
    df['最后更新'] = df['最后更新'].apply(lambda x: str(datetime.timedelta(minutes=x)))
    df.reset_index(drop=True,inplace=True)
    df.to_csv(path)


if __name__ == '__main__':
    path = '1/soft.csv'
    headers = {
        "Host": "yz.chsi.com.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "123",
        "Origin": "https://yz.chsi.com.cn",
        "Connection": "keep-alive",
        "Referer": "https://yz.chsi.com.cn/sytj/tj/qecx.html",
        "Cookie":"JSESSIONID=F78B519DCA2C8F84F656B3439BC1BFF3; zg_did=%7B%22did%22%3A%20%22177ce11ae02410-015d12619143a5-111a4459-fa000-177ce11ae0316d9%22%7D; _ga=GA1.3.250539756.1614070001; aliyungf_tc=be9fef0c7b754e9bdbc5b544081bb314d5d522f43d0627b24e9668d5f9846ebb; XSRF-CCKTOKEN=ed5451ef9776792c1cfb06e48998d7ab; CHSICC_CLIENTFLAGZSML=de3901ac561c306945606f900cc38fa4; CHSICC_CLIENTFLAGCHSI=60249618f504ea500b03b52cc74a9807; __utmc=65168252; __utmz=65168252.1616135295.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=65168252.250539756.1614070001.1616135295.1616149537.2; CHSICC_CLIENTFLAGSYTJ=600c1a2c04ece3603c4571d5271b2258; zg_0d76434d9bb94abfaa16e1d5a3d82b52=%7B%22sid%22%3A%201616227817437%2C%22updated%22%3A%201616227967400%2C%22info%22%3A%201616227817443%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fmy.chsi.com.cn%2Farchive%2Findex.jsp%22%2C%22cuid%22%3A%20%22d39c22684570c457d37100fc10fd1afc%22%7D; zg_14e129856fe4458eb91a735923550aa6=%7B%22sid%22%3A%201616227804299%2C%22updated%22%3A%201616227976333%2C%22info%22%3A%201616227804300%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fwww.chsi.com.cn%2F%22%7D; CHSICC_CLIENTFLAGYZ=c7e0098c321dff96d500c87e4a5d425c; zg_288ab1c4d4ac4d22b9a811f177cc6228=%7B%22sid%22%3A%201616386946554%2C%22updated%22%3A%201616387146735%2C%22info%22%3A%201616384022686%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fbm.chsi.com.cn%2Fycms%2Fkssysm%2F%22%7D; CHSICC_CLIENTFLAGAPPLY=89dcb5a0207318b4fdf1ab15c6445aa3; CHSICC_CLIENTFLAGTMGK=5c19ef3b20707c6d27d83b267ac3a281; _gid=GA1.3.1942029628.1616896164; JSESSIONID=702028C40A0B56A9968F1C8B46F2667F; acw_tc=2f6fc12c16176707912264127ec6a5c9c969756120a7ca559b694dc5ec65a5; zg_adfb574f9c54457db21741353c3b0aa7=%7B%22sid%22%3A%201617670932837%2C%22updated%22%3A%201617670932837%2C%22info%22%3A%201617602200401%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22yz.chsi.com.cn%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fyz.chsi.com.cn%2F%22%2C%22cuid%22%3A%20%22d39c22684570c457d37100fc10fd1afc%22%7D",
        "Cache-Control": "no-cache"
    }  
    if os.path.exists(path):
        os.remove(path)
    for page in range(100):
        content = find_school(page,"大学",headers) 
        parse_one_page(content)
        for item in parse_one_page(content):
            with open(path, 'a', encoding='utf-8') as csv:
                csv.write(
                    item['school'] + ',' +
                    item['academic'] + ',' + 
                    item['major'] + ',' + 
                    item['direction'] + ',' + 
                    str(item['type']) + ',' +
                    str(item['remain']) + ',' + 
                    str(item['publish']) + ',' +
                    item['fit'] + ',' + 
                    item['test_requirement'] + ',' +
                    str(item['conditions']) + 
                    '\n' 
                    )
    data_processing(path)

