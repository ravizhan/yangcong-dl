import re

import decrypt
import download
import json
import requests


class yc:
    def __init__(self):
        while True:
            try:
                choice1 = int(input('1.手动输入authorization   2.账号密码登录\n请选择登陆方式:'))
                if choice1 in [1, 2]:
                    break
                else:
                    continue
            except Exception or ValueError:
                continue
        if choice1 == 1:
            self.authorization = input('authorization:')
        elif choice1 == 2:
            print('用户登录')
            username = input('用户名(手机号):')
            pw = input('密码:')
            self.authorization = self.login(username, pw)
        self.header = {
            'Authorization': self.authorization,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"
        }

    def getkey(self, dic, value_list):
        res = []
        for value in list(value_list):
            res.append(list(dic.keys())[list(dic.values()).index(str(value))])
        return res

    def login(self, username, pw):
        data = '{"name":"%s","password":"%s"}' % (username, pw)
        header = {
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"
        }
        res = requests.post('https://school-api.yangcong345.com/public/login', data=data, headers=header).headers
        return res['authorization']

    def get_themesid(self, url):
        res1 = requests.get(url, headers=self.header).text
        themes_ids, res = [], []
        res1 = json.loads(res1)
        for a in range(0, 10):
            try:
                themes_ids.append(res1[a]['sections'][0]['subsections'][0]['themes'][0]['id'])
            except Exception:
                continue
            for b in range(0, 10):
                try:
                    themes_ids.append(res1[a]['sections'][b]['subsections'][0]['themes'][0]['id'])
                except Exception:
                    continue
                for c in range(0, 10):
                    try:
                        themes_ids.append(res1[a]['sections'][b]['subsections'][c]['themes'][0]['id'])
                        themes_ids.append(res1[a]['sections'][b]['subsections'][c]['themes'][1]['id'])
                    except Exception:
                        continue
        for id in themes_ids:
            if id not in res:
                res.append(id)
        return res

    # def get_themesid_special(self, url):
    #     data = requests.get(url, headers=self.header).text
    #     res = []
    #     data = json.loads(data)["levels"]
    #     pattern = re.compile('''videoId": ".{36}''')
    #     for i in pattern.findall(json.dumps(data)):
    #         res.append(str(i).replace('''videoId": "''',''))
    #     return res

    def get_names(self, url):
        res1 = requests.get(url, headers=self.header).text
        names, res = [], []
        res1 = json.loads(res1)
        for a in range(0, 10):
            try:
                names.append(res1[a]['name'])
            except Exception:
                continue
            for b in range(0, 10):
                try:
                    names.append(res1[a]['sections'][b]['name'])
                except Exception:
                    continue
                for c in range(0, 10):
                    try:
                        names.append(res1[a]['sections'][b]['subsections'][c]['name'])
                    except Exception:
                        continue
                    for d in range(0, 10):
                        try:
                            names.append(res1[a]['sections'][b]['subsections'][c]['themes'][d]['name'])
                        except Exception:
                            continue
        for id in names:
            if id not in res:
                res.append(id)
        return res

    def get_m3u8_url(self, themes_id):
        url2 = 'https://school-api.yangcong345.com/course/course-tree/themes/' + themes_id
        text = json.loads(requests.get(url2, headers=self.header).text)["encrypt_body"]
        res2 = decrypt.dec(text)
        m3u8_urls, names = [], []
        for i in range(0, 10):
            try:
                for a in range(0, 10):
                    m3u8_url = res2['topics'][i]['video']['addresses'][a]['url']
                    platform = res2['topics'][i]['video']['addresses'][a]['platform']
                    format = res2['topics'][i]['video']['addresses'][a]['format']
                    clarity = res2['topics'][i]['video']['addresses'][a]['clarity']
                    if platform == 'pc' and format == 'hls' and clarity == 'high':
                        if m3u8_url not in m3u8_urls:
                            m3u8_urls.append(m3u8_url)
            except Exception:
                continue
            try:
                name = res2['topics'][i]['name']
                names.append(name)
                # print(m3u8_url)
            except Exception:
                continue
        return m3u8_urls, names

    # def get_m3u8_url_special(self, themes_id):
    #     url2 = 'https://school-api.yangcong345.com/course/course-tree/themes/' + themes_id
    #     text = json.loads(requests.get(url2, headers=self.header).text)["encrypt_body"]
    #     res2 = decrypt.dec(text)
    #     m3u8_urls, names = [], []
    #     for i in range(0, 10):
    #         try:
    #             for a in range(0, 10):
    #                 m3u8_url = res2['topics'][i]['video']['addresses'][a]['url']
    #                 platform = res2['topics'][i]['video']['addresses'][a]['platform']
    #                 format = res2['topics'][i]['video']['addresses'][a]['format']
    #                 clarity = res2['topics'][i]['video']['addresses'][a]['clarity']
    #                 if platform == 'pc' and format == 'hls' and clarity == 'high':
    #                     if m3u8_url not in m3u8_urls:
    #                         m3u8_urls.append(m3u8_url)
    #         except Exception:
    #             continue
    #         try:
    #             name = res2['topics'][i]['name']
    #             names.append(name)
    #             # print(m3u8_url)
    #         except Exception:
    #             continue
    #     return m3u8_urls, names

    def chooce(self):
        data = json.loads(requests.get("https://school-api.yangcong345.com/course/subjects", headers=self.header).text)
        # print("学科")
        for i in data:
            print(i["id"], i["name"])
        subject_id = int(input("请输入学科 对应的的序号:"))
        temp = {}
        for i in range(len(data)):
            id = data[i]["id"]
            name = data[i]["name"]
            if id == subject_id:
                temp["subject"] = {"index": i, "id": id, "name": name}

        # print("阶段")
        index = temp["subject"]["index"]
        data = data[index]["stages"]
        for i in data:
            print(i["id"], i["name"])
        stage_id = int(input("请输入阶段 对应的的序号:"))
        for i in range(len(data)):
            id = data[i]["id"]
            name = data[i]["name"]
            if id == stage_id:
                temp["stage"] = {"index": i, "id": id, "name": name}

        # url = 'https://school-api.yangcong345.com/course-tree/recommend-special-courses?stageId=%s&subjectId=%s' % (
        # temp["stage"]["id"], temp["subject"]["id"])
        # special = json.loads(requests.get(url, headers=self.header).text)
        # if len(special) != 0:
        #     print("检测到专题课，是否下载")
        #     choose = int(input("1.下载 2.跳过\n请输入:"))
        #     if choose == 1:
        #         download_dir = temp["subject"]["name"] + "/" + temp["stage"]["name"]
        #         return "https://school-api.yangcong345.com/course/special-course/"+special[0]["id"], download_dir
        # print("版本")
        index = temp["stage"]["index"]
        data = data[index]["publishers"]
        for i in data:
            print(i["id"], i["name"])
        publisher_id = int(input("请输入版本 对应的的序号:"))
        for i in range(len(data)):
            id = data[i]["id"]
            name = data[i]["name"]
            if id == publisher_id:
                temp["publisher"] = {"index": i, "id": id, "name": name}

        # print("学期")
        index = temp["publisher"]["index"]
        data = data[index]["semesters"]
        for i in data:
            print(i["id"], i["name"])
        semester_id = int(input("请输入学期 对应的的序号:"))
        for i in range(len(data)):
            id = data[i]["id"]
            name = data[i]["name"]
            if id == semester_id:
                temp["semester"] = {"index": i, "id": id, "name": name}
        print(temp)
        url = "https://school-api.yangcong345.com/course/chapters-with-section/publisher/%s/semester/%s/subject/%s/stage/%s" % (
            temp["publisher"]["id"], temp["semester"]["id"], temp["subject"]["id"], temp["stage"]["id"],)
        # print(url)
        download_dir = temp["subject"]["name"] + "/" + temp["publisher"]["name"] + "/" + temp["semester"]["name"]
        return url, download_dir


if __name__ == '__main__':
    yangcong = yc()
    url, download_dir = yangcong.chooce()
    themes_ids = []
    # if "special" in url:
    #     list1 = yangcong.get_themesid_special(url)
    # else:
    #     list1 = yangcong.get_themesid(url)
    [themes_ids.append(i) for i in list1 if i not in themes_ids]
    m3u8_urls, video_names = [], []
    for i in range(0, len(themes_ids)):
        print('\r进度:%d/%d' % (i + 1, len(themes_ids)), end='')
        a, b = yangcong.get_m3u8_url(themes_ids[i])
        m3u8_urls.append(a)
        video_names.append(b)
    print('\n爬取完成')
    m3u8_urls = [i for j in m3u8_urls for i in j]
    video_names = [i for j in video_names for i in j]
    for i in range(0, len(m3u8_urls)):
        print(str(i + 1) + '.' + video_names[i])
    while True:
        try:
            choose = input('请输入要下载的序号(用英文逗号分隔)(全部直接回车):')
            if choose == '':
                break
            choose = choose.split(',')
            break
        except:
            pass
    if choose == '':
        print('开始下载')
        download.download(m3u8_urls, video_names, download_dir)
    elif choose != '':
        res_m3u8_urls, res_video_names = [], []
        for i in choose:
            res_m3u8_urls.append(m3u8_urls[int(i) - 1])
            res_video_names.append(video_names[int(i) - 1])
        print('开始下载')
        download.download(res_m3u8_urls, res_video_names, download_dir)
