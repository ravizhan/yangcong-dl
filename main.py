import requests,json,download,decrypt

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
            'Authorization': self.authorization
        }

    def getkey(self,dic, value_list):
        res = []
        for value in list(value_list):
            res.append(list(dic.keys())[list(dic.values()).index(str(value))])
        return res

    def login(self,username, pw):
        data = '{"name":"%s","password":"%s"}' % (username, pw)
        header = {
            'Content-Type': 'application/json'
        }
        res = requests.post('https://school-api.yangcong345.com/public/login', data=data, headers=header).headers
        return res['authorization']

    def get_themesid(self):
        res1 = requests.get(url1, headers=self.header).text
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

    def get_names(self):
        res1 = requests.get(url1, headers=self.header).text
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

    def get_m3u8_url(self,themes_id):
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
                    if (platform == 'pc' and format == 'hls' and clarity == 'high'):
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

    def chooce(self):
        subject, publisher = '', ''
        subjects = {
            '小学数学': '1',
            '初中数学': '1',
            '高中数学': '1',
            '初中物理': '2',
            '初中化学': '4',
        }
        publishers = {
            '人教版': '1',
            '北师大版': '2',
            '华师大版': '3',
            '湘教版': '4',
            '冀教版': '5',
            '苏科版': '6',
            '鲁教版': '7',
            '沪科版': '8',
            '沪教版': '9',
            '青岛版': '10',
            '浙教版': '11',
            '北京课改版': '12',
            '通用版': '13',
            '鲁科版': '14',
            '苏教版': '15',
            '粤沪版': '16',
            '教科版': '17',
            '人教A': '18',
            '人教B': '19',
            '湘教旧版': '20',
            '人教新课标A': '21',
            '青岛版(五·四学制)':'22',
            '人教新课标B': '24',
            '苏教版(新课标)':'26',
            '北师大版(新课标)':'27'
        }
        semesters = {
            '三年级上册': '5',
            '三年级下册': '6',
            '四年级上册': '7',
            '四年级下册': '8',
            '五年级上册': '9',
            '五年级下册': '10',
            '六年级上册': '11',
            '六年级下册': '12',
            '七年级上册': '13',
            '七年级下册': '14',
            '八年级上册': '15',
            '八年级下册': '16',
            '九年级上册': '17',
            '九年级下册': '18',
            '八年级全一册': '31',
            '九年级全一册': '32',
            '中考一轮': '33',
            '中考二轮': '34',
            '中考总复习':'44',
            '必修一': '19',
            '必修二': '20',
            '必修三': '21',
            '必修四': '22',
            '必修五': '23',
            '选修2-1(理科)': '29',
            '选修2-2(理科)': '36',
            '选修2-3(理科)': '40',
            '选修1-1(文科)': '41',
            '选修1-2(文科)': '42',
            '必修上':'25',
            '必修下':'26',
            '选修一上册':'28',
            '选修一下册':'35',
            '选择性必修第一册':'45',
            '选择性必修第二册': '46',
            '选择性必修第三册': '47',
        }
        for i in range(len(list(subjects.keys()))):
            print(str(i) + '.' + list(subjects.keys())[i] + '  ', end='')
        while True:
            try:
                choice_sub = int(input('\n请输入要下载的学科的序号:'))
                subject = subjects[list(subjects.keys())[choice_sub]]
                break
            except Exception or ValueError:
                continue
        if list(subjects.keys())[choice_sub] == '小学数学':
            for i in [1, 2, 5, 6, 10, 22]: print(str(i) + '.' + list(publishers.keys())[i - 1] + '  ', end='')
        elif list(subjects.keys())[choice_sub] == '初中数学':
            for i in range(1, 14): print(str(i) + '.' + list(publishers.keys())[i - 1] + '  ', end='')
        elif list(subjects.keys())[choice_sub] == '高中数学':
            for i in [1, 2, 4, 15, 18, 19, 20,21,23,24,25]: print(str(i) + '.' + list(publishers.keys())[i - 1] + '  ',end='')
        elif list(subjects.keys())[choice_sub] == '初中物理':
            for i in [1,2,6,8,9,11,12,14,16,17]: print(str(i) + '.' + list(publishers.keys())[i - 1] + '  ', end='')
        elif list(subjects.keys())[choice_sub] == '初中化学':
            for i in [1,7,9,11]: print(str(i) + '.' + list(publishers.keys())[i - 1] + '  ', end='')
        while True:
            try:
                choice = int(input('\n请输入版本的序号:'))
                publisher = publishers[list(publishers.keys())[choice-1]]
                break
            except Exception or ValueError:
                continue
        if list(subjects.keys())[choice_sub] == '小学数学':
            for i in range(1, 9): print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
        elif list(subjects.keys())[choice_sub] == '初中数学':
            for i in [9,10,11,12,13,14,17,18]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
        elif list(subjects.keys())[choice_sub] == '高中数学':
            if int(publisher) in [1,2,15,18,19,20]:
                for i in range(20, 29): print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 4:
                for i in range(27, 31): print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 21:
                for i in [20,21,34,35]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 24:
                for i in [20,21,22,23,34,35,36]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 26:
                for i in [20, 21]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 27:
                for i in [20,21,34]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
        elif list(subjects.keys())[choice_sub] == '初中物理':
            if int(publisher) in [1,2]:
                for i in [11,12,16]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) in [6,7,9,16,17]:
                for i in range(11,15): print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) in [8,12]:
                for i in [15,16]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 11:
                for i in range(9,14): print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
        elif list(subjects.keys())[choice_sub] == '初中化学':
            if int(publisher) in [1,9]:
                for i in [13,14,19]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 7:
                for i in [15,16,19]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
            elif int(publisher) == 11:
                for i in [9,11,12,13,19]: print(str(i) + '.' + list(semesters.keys())[i - 1] + '  ', end='')
        while True:
            try:
                choice = int(input('\n请输入年级的序号:'))
                semester = int(semesters[list(semesters.keys())[choice-1]])
                # print(list(subjects.keys())[choice_sub])
                if list(subjects.keys())[choice_sub] == '小学数学' and choice in range(1, 9):
                    break
                elif list(subjects.keys())[choice_sub] in ['初中数学','初中化学','初中物理'] and choice in range(9, 20):
                    break
                elif list(subjects.keys())[choice_sub] == '高中数学' and choice in range(20, 37):
                    break
                else:
                    continue
            except Exception or ValueError:
                continue
        print('正在爬取')
        # print(semester)
        if semester <= 12:
            stage = '1'
        elif 18 >= semester > 12:
            stage = '2'
        elif semester in range(31,45):
            stage = '2'
        else:
            stage = '3'
        url = 'https://school-api.yangcong345.com/course/chapters-with-section/publisher/%s/semester/%s/subject/%s/stage/%s' % (
        publisher, semester, subject, stage)
        # print(url)
        download_dir = publisher+str(semester)+subject
        return url,download_dir


if __name__ == '__main__':
    yangcong = yc()
    url1,download_dir = yangcong.chooce()
    themes_ids = []
    list1 = yangcong.get_themesid()
    [themes_ids.append(i) for i in list1 if i not in themes_ids]
    m3u8_urls, video_names = [], []
    for i in range(0,len(themes_ids)):
        print('\r进度:%d/%d'%(i+1,len(themes_ids)),end='')
        a,b = yangcong.get_m3u8_url(themes_ids[i])
        m3u8_urls.append(a)
        video_names.append(b)
    print('\n爬取完成')
    m3u8_urls = [i for j in m3u8_urls for i in j]
    video_names = [i for j in video_names for i in j]
    for i in range(0,len(m3u8_urls)):
        print(str(i+1)+'.'+video_names[i])
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
        download.download(m3u8_urls, video_names,download_dir)
    elif  choose != '':
        res_m3u8_urls,res_video_names = [],[]
        for i in choose:
            res_m3u8_urls.append(m3u8_urls[int(i)-1])
            res_video_names.append(video_names[int(i)-1])
        print('开始下载')
        download.download(res_m3u8_urls, res_video_names,download_dir)

