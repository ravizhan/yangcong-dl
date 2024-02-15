import base64
import json
import random
import string

import requests

import decrypt
import download


class YC:
    def __init__(self):
        while True:
            try:
                choice = int(input('1.手动输入authorization   2.账号密码登录\n请选择登陆方式:'))
                if choice in [1, 2]:
                    break
                else:
                    continue
            except Exception or ValueError:
                continue
        if choice == 1:
            while True:
                self.authorization = input('authorization:')
                if self.authorization.startswith("Bearer"):
                    break
                print("authorization格式错误")
        elif choice == 2:
            while True:
                print('用户登录')
                username = input('用户名(手机号):')
                pw = input('密码:')
                self.authorization = self.login(username, pw)
                if self.authorization is not None:
                    break
                print("登陆失败")
        rand_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        self.header = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Omvd": "yangcong345" + base64.b64encode(rand_string.encode()).decode(),
            "Authorization": self.authorization,
            "Refer": "https://school.yangcongxueyuan.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }

    def login(self, username, password) -> str or None:
        """
        账户密码登录
        :param username: 用户名/手机号
        :param password: 密码
        :return: authorization
        """
        data = '{"name":"%s","password":"%s"}' % (username, password)
        header = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        res = requests.post('https://school-api.yangcong345.com/public/login', data=data, headers=header).headers
        if "authorization" in res:
            return res['authorization']
        else:
            return None

    def get_topic_and_name(self, data: dict, unit_list: list) -> (list, list):
        """
        获取topic id列表和视频名字列表
        :param data: 课程数据
        :param unit_list: 选择的单元列表
        :return: topic id列表和视频名字列表
        """
        topic_ids = []
        name_list = []
        theme_ids = []
        for item in data:
            if item["name"] not in unit_list:
                continue
            for section in item["sections"]:
                for subsection in section["subsections"]:
                    for theme in subsection["themes"]:
                        theme_ids.append(theme["id"])
                        for topic in theme["topics"]:
                            topic_ids.append(topic["id"])
                            name_list.append(topic["name"])
        return theme_ids, topic_ids, name_list

    def api_1(self, theme_id, topic_ids):
        url = 'https://school-api.yangcong345.com/course/course-tree/themes/' + theme_id
        text = json.loads(requests.get(url, headers=self.header).text)["encrypt_body"]
        res = decrypt.decrypt(text)
        video_urls = []
        for topic in res["topics"]:
            if topic["id"] not in topic_ids:
                continue
            for video in topic["video"]["addresses"]:
                if video["platform"] == "pc" and video["format"] == "hls" and video["clarity"] == "high":
                    if video["url"] is None:
                        print("接口1失效")
                        raise Exception
                    video_urls.append(video["url"])
        return video_urls

    def api_2(self, topic_id):
        url = f"https://school-api.yangcong345.com/course/topics/{topic_id}/detail-universal"
        data = requests.get(url, headers=self.header).json()
        print(data)
        for i in data["video"]["addresses"]:
            if i["clarity"] == "high" and i["format"] == "hls" and i["platform"] == "pc":
                if i["url"] is None:
                    print("接口2失效")
                    raise Exception
                return i["url"]

    def choose(self):
        data = json.loads(requests.get("https://school-api.yangcong345.com/course/subjects", headers=self.header).text)
        # print("学科")
        for i in data:
            print(i["id"], i["name"])
        while True:
            try:
                subject_id = int(input("请输入学科 对应的的序号:"))
                if subject_id in [int(i["id"]) for i in data]:
                    break
                print("输入错误")
            except Exception:
                print("输入错误")
                continue
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
        while True:
            try:
                stage_id = int(input("请输入阶段 对应的的序号:"))
                if stage_id in [int(i["id"]) for i in data]:
                    break
                print("输入错误")
            except Exception:
                print("输入错误")
                continue
        for i in range(len(data)):
            id = data[i]["id"]
            name = data[i]["name"]
            if id == stage_id:
                temp["stage"] = {"index": i, "id": id, "name": name}

        # print("版本")
        index = temp["stage"]["index"]
        data = data[index]["publishers"]
        for i in data:
            print(i["id"], i["name"])
        while True:

            try:
                publisher_id = int(input("请输入版本 对应的的序号:"))
                if publisher_id in [int(i["id"]) for i in data]:
                    break
                print("输入错误")
            except Exception:
                print("输入错误")
                continue
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
        while True:
            try:
                semester_id = int(input("请输入学期 对应的的序号:"))
                if semester_id in [int(i["id"]) for i in data]:
                    break
                print("输入错误")
            except Exception:
                print("输入错误")
                continue
        for i in range(len(data)):
            id = data[i]["id"]
            name = data[i]["name"]
            if id == semester_id:
                temp["semester"] = {"index": i, "id": id, "name": name}

        # print(temp)
        url = "https://school-api.yangcong345.com/course/chapters-with-section/scene?publisherId=%s&semesterId=%s&subjectId=%s&stageId=%s" % (
            temp["publisher"]["id"], temp["semester"]["id"], temp["subject"]["id"], temp["stage"]["id"],)
        # print(url)
        data = requests.get(url, headers=self.header).json()
        for i in range(len(data)):
            print(i, data[i]["name"])
        unit = input("请输入单元 对应的的序号(用空格分隔)(全部直接回车):")
        if unit == '':
            unit_list = [data[i]["name"] for i in range(0, len(data))]
        else:
            unit_list = [data[int(i)]["name"] for i in unit.split(" ")]
        download_dir = temp["subject"]["name"] + "/" + temp["publisher"]["name"] + "/" + temp["semester"]["name"]
        return data, unit_list, download_dir


if __name__ == '__main__':
    yangcong = YC()
    try:
        data, unit_list, download_dir = yangcong.choose()
    except Exception as e:
        print(e)
        print('未知错误')
        input("按任意键退出")
    theme_ids, topic_ids, names = yangcong.get_topic_and_name(data, unit_list)
    for i in range(0, len(names)):
        print(str(i) + ' ' + names[i])
    while True:
        try:
            choice = input('请输入要下载的序号(用空格分隔)(全部直接回车):')
            if choice == '':
                break
            choice = choice.split(' ')
            break
        except Exception:
            pass
    if choice == '':
        video_names, video_urls = names, []
        try:
            for i in range(0, len(theme_ids)):
                video_urls = video_urls + yangcong.api_1(theme_ids[i], topic_ids)
                print('\r爬取进度:%d/%d' % (len(video_urls), len(video_names)), end='')
                if len(video_urls) == len(video_names):
                    break
        except Exception:
            print("接口1出错")
            video_urls = []
            for i in range(0, len(topic_ids)):
                print('\r爬取进度:%d/%d' % (i + 1, len(topic_ids)), end='')
                video_urls.append(yangcong.api_2(topic_ids[i]))
    else:
        video_names, video_urls = [names[int(i)] for i in choice], []
        try:
            for i in range(0, len(theme_ids)):
                temp_topic_ids = [topic_ids[int(i)] for i in choice]
                video_urls = video_urls + yangcong.api_1(theme_ids[i], temp_topic_ids)
                print('\r爬取进度:%d/%d' % (len(video_urls), len(choice)), end='')
                if len(video_urls) == len(video_names):
                    break
        except Exception:
            print("接口1出错")
            video_urls = []
            for i in range(0, len(choice)):
                print('\r爬取进度:%d/%d' % (i + 1, len(choice)), end='')
                video_urls.append(yangcong.api_2(topic_ids[int(choice[i])]))
    print('\n爬取完成')
    print('开始下载')
    download.download(video_urls, video_names, download_dir)
