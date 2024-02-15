import base64
import json
import random
import string
import os

import requests

import decrypt


class YCForWeb:
    def __init__(self, startmode, choice=None, a=None, b=None):
        self.all_data = None
        self.data = None
        self.topic_ids = []
        self.name_list = []
        self.theme_ids = []
        self.error = None
        if startmode == 0:
            if choice == 0:
                self.authorization = a
                if self.authorization.startswith("Bearer"):
                    pass
                else:
                    self.error = "Error authorization错误"
            elif choice == 1:
                self.login(username=a, password=b)
                if self.authorization is not None:
                    pass
                else:
                    self.error = "Error 账密登录错误"
        else:
            with open('authorization.txt', 'r') as f:
                self.authorization = f.read()

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

    def login(self, username, password) -> bool:
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
            self.authorization = res['authorization']
            return True
        else:
            return False

    def checkError(self):
        if self.error == None:
            return [None, False]
        return [self.error, True]

    def save_authorization(self):
        with open("authorization.txt", "w") as f:
            f.write(self.authorization)

    def delete_authorization(self):
        try:
            os.remove('authorization.txt')
        except Exception:
            pass

    def first_choose(self) -> (dict, str):
        """
        获取版本、学期、学科、阶段名称及ID
        :return: 版本、学期、学科、阶段名称及ID
        """
        self.data = requests.get("https://school-api.yangcong345.com/course/subjects", headers=self.header).json()
        return self.data, json.dumps(self.data)

    def second_choose(self, publisher_id: str, semester_id: str, subject_id: str, stage_id: str) -> (list, str):
        """
        获取单元列表
        :param publisher_id: 版本ID
        :param semester_id: 学期ID
        :param subject_id: 学科ID
        :param stage_id: 阶段ID
        :return: 单元列表和下载路径
        """
        url = f"https://school-api.yangcong345.com/course/chapters-with-section/scene?publisherId={publisher_id}&semesterId={semester_id}&subjectId={subject_id}&stageId={stage_id}"
        self.all_data = requests.get(url, headers=self.header).json()
        subject = None
        publisher = None
        semester = None
        for data in self.data:
            if data["id"] == int(subject_id):
                subject = data["name"]
                for stage_data in data["stages"]:
                    if stage_data["id"] == int(stage_id):
                        for publisher_data in stage_data["publishers"]:
                            if publisher_data["id"] == int(publisher_id):
                                publisher = publisher_data["name"]
                                for semester_data in publisher_data["semesters"]:
                                    if semester_data["id"] == int(semester_id):
                                        semester = semester_data["name"]
                                        break
                                break
                        break
                break
        path = f"{subject}/{publisher}/{semester}"
        return [self.all_data[i]["name"] for i in range(len(self.all_data))], path

    def get_topic_and_name(self, unit_list: list) -> (list, list, list):
        """
        :param unit_list: 单元列表 例: ["第一单元",···]
        :return: theme_ids, topic_ids, name_list(视频名称列表)
        """
        self.theme_ids, self.topic_ids, self.name_list = [], [], []
        for item in self.all_data:
            if item["name"] not in unit_list:
                continue
            for section in item["sections"]:
                for subsection in section["subsections"]:
                    for theme in subsection["themes"]:
                        self.theme_ids.append(theme["id"])
                        for topic in theme["topics"]:
                            self.topic_ids.append(topic["id"])
                            self.name_list.append(topic["name"])
        return self.theme_ids, self.topic_ids, self.name_list

    def api_1(self, theme_id: str, topic_ids: list) -> list:
        """
        视频解析接口1
        :param theme_id: theme_ids中的theme_id
        :param topic_ids: topic_ids中多个topic_id组成的列表
        :return: topic_ids对应的视频地址列表
        """
        url = 'https://school-api.yangcong345.com/course/course-tree/themes/' + theme_id
        text = json.loads(requests.get(url, headers=self.header).text)["encrypt_body"]
        res = decrypt.decrypt(text)
        video_urls = []
        for topic in res["topics"]:
            if topic["id"] not in topic_ids:
                continue
            for video in topic["video"]["addresses"]:
                if video["platform"] == "pc" and video["format"] == "hls" and video["clarity"] == "fullHigh":
                    if video["url"] is None:
                        raise Exception
                    video_urls.append(video["url"])
        if len(video_urls) == 0:
            # print('(High画质)')
            for topic in res["topics"]:
                if topic["id"] not in topic_ids:
                    continue
                for video in topic["video"]["addresses"]:
                    if video["platform"] == "pc" and video["format"] == "hls" and video["clarity"] == "high":
                        if video["url"] is None:
                            raise Exception
                        video_urls.append(video["url"])
        return video_urls

    def api_2(self, topic_id) -> str:
        """
        视频解析接口2
        :param topic_id: topic_ids中特定的一个topic_id
        :return: topic_id对应的视频地址
        """
        url = f"https://school-api.yangcong345.com/course/topics/{topic_id}/detail-universal"
        data = requests.get(url, headers=self.header).json()
        print(data)
        for i in data["video"]["addresses"]:
            if i["clarity"] == "high" and i["format"] == "hls" and i["platform"] == "pc":
                if i["url"] is None:
                    raise Exception
                return i["url"]

    def get_download_url(self, chosen_topic_ids: list) -> list or None:
        """
        调用下载api
        :param chosen_topic_ids: 选择的topic_id列表
        :return: m3u8地址列表
        """
        video_names, video_urls = [], []
        for topic_id in chosen_topic_ids:
            index = self.topic_ids.index(topic_id)
            video_names.append(self.name_list[index])
        try:
            for i in range(0, len(self.theme_ids)):
                video_urls = video_urls + self.api_1(self.theme_ids[i], chosen_topic_ids)
                print('\r爬取进度:%d/%d' % (len(video_urls), len(chosen_topic_ids)), end='')
                if len(video_urls) == len(chosen_topic_ids):
                    break
            return video_urls
        except Exception:
            print("接口1出错")
            try:
                video_urls = []
                for i in range(0, len(chosen_topic_ids)):
                    video_urls.append(self.api_2(self.topic_ids[i]))
                    print('\r爬取进度:%d/%d' % (i + 1, len(chosen_topic_ids)), end='')
                return video_urls
            except Exception:
                print("接口2出错")
                return None
