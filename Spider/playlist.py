# -*- coding: utf-8 -*-
import re
import csv
import json
import time
import pymysql
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

# 请求头
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

# 歌单类型链接
type_url = "https://music.163.com/discover/playlist"

# 连接数据库
db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "123",
    port=3306,
    db = "cloudmusic"
        )

cursor = db.cursor()


"""获取歌单类型"""
def get_playlist_type(url):
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    types = [t.text for t in soup.select("a.s-fc1")][1:]
    return types


"""获取歌单id"""
def get_playlist_id(url):
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    ids = [re.sub(r"\D+", "", i['href']) for i in soup.select("a.msk")]
    t = re.search('https.*cat=(.*)&limit', url).group(1)
    get_playlist_info(ids, t)
    

"""获取歌单信息"""
def get_playlist_info(ids, t):
    playlist_url = "https://api.imjad.cn/cloudmusic/?type=playlist&id={}"
    urls = [playlist_url.format(i) for i in ids]
    
    for url in urls:
        try:
            response = requests.get(url=url, headers=headers)
            json_text = response.text
            json_playlist = json.loads(json_text)["playlist"]
        except:
            continue
        
        # 歌单ID、歌单名、歌单类型、标签、创建时间、最后更新时间、播放量、收藏量、转发量、评论数
        # 用户名、性别、用户类型、VIP类型、省份、城市
        playlistID = str(json_playlist["id"])
        name = json_playlist["name"]
        playlistType = t
        tags = "、".join(json_playlist["tags"])
        createTime = time.strftime("%Y-%m-%d", time.localtime(int(str(json_playlist["createTime"])[:-3])))
        updateTime = time.strftime("%Y-%m-%d", time.localtime(int(str(json_playlist["updateTime"])[:-3])))
        tracks_num = len(json_playlist["trackIds"])
        playCount = json_playlist["playCount"]
        subscribedCount = json_playlist["subscribedCount"]
        shareCount = json_playlist["shareCount"]
        commentCount = json_playlist["commentCount"]
        nickname = json_playlist['creator']['nickname']
        gender = str(json_playlist['creator']['gender'])
        userType = str(json_playlist['creator']['userType'])
        vipType = str(json_playlist['creator']['vipType'])
        province = str(json_playlist['creator']['province'])
        city = str(json_playlist['creator']['city'])
        
        # 匹配性别、省份、城市代码
        if gender == '1':
            gender = '男'
        else:
            gender = '女'
        
        # 打开行政区代码文件
        with open("country.csv", encoding="utf-8") as f:
            rows = csv.reader(f)
        
            for row in rows:
                if row[0] == province:
                    province = row[1]
                if row[0] == city:
                    city = row[1]
            
            if province == '香港特别行政区':
                city = '香港特别行政区'
            if province == '澳门特别行政区':
                city = '澳门特别行政区'
            if province == '台湾省':
                city = '台湾省'
            if province == str(json_playlist['creator']['province']):
                province = '海外'
                city = '海外'
            if city == str(json_playlist['creator']['city']):
                city = province
        
        playlist = [playlistID, name, playlistType, tags, createTime, updateTime,
                    tracks_num, playCount, subscribedCount, shareCount, commentCount,
                    nickname, gender, userType, vipType, province, city]
        print(playlist)
        save_to_playlists(playlist)
        


"""保存到数据库"""
def save_to_playlists(l):
    sql = """insert into playlists(id, name, type, tags, create_time, update_time, 
                tracks_num, play_count, subscribed_count, share_count, comment_count, nickname,
                gender, user_type, vip_type, province, city)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(sql, (l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11],l[12],l[13],l[14],l[15],l[16]))
        db.commit()
    except:
        db.rollback()


def main():
    types = get_playlist_type(type_url)
    
    urls = []
    for t in types:
        for i in range(37):
            url = "https://music.163.com/discover/playlist/?order=hot&cat={0}&limit=35&offset={1}".format(t, i*35)
            urls.append(url)

    
    pool = Pool(10)
    for url in urls:
        pool.apply_async(get_playlist_id, args=(url,))
    pool.close()
    pool.join()



if __name__ == "__main__":
    main()


