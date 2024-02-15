import os
import zipfile
from time import sleep
from requests import get
import threading

global waitForNewDownloadTime
waitForNewDownloadTime = 2.25


def count_mp4_files(directory):
    try:
        return len([name for name in os.listdir(directory) if name.endswith('.mp4') and os.path.isfile(os.path.join(directory, name))])
    except:
        return 0


def checkDone(directory, all):
    get_url = True
    last = 0
    # 循环检查直到没有文件夹
    while True:
        sleep(0.25)
        current_count = count_mp4_files(directory)
        try:
            if get_url and last != current_count:
                url = 'http://127.0.0.1:5000/progress_up?data=' + str(current_count)
                get(url)
        except:
            get_url = False
        os.system('cls')
        print(f"下载进度： {current_count}/{all}(Videos)")
        last = current_count
        if current_count == all:
            break

    print("done")


def download(urls, names, download_dir):
    global waitForNewDownloadTime
    if not os.path.exists('N_m3u8DL-CLI_v3.0.2.exe') or not os.path.exists('ffmpeg.exe'):
        print('未检测到下载器,开始下载')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        try:
            zip = get(
                'https://mirror.ghproxy.com/https://github.com/nilaoda/N_m3u8DL-CLI/releases/download/3.0.2/N_m3u8DL-CLI_v3.0.2_with_ffmpeg_and_SimpleG.zip',
                headers=headers).content
            with open('N_m3u8DL-CLI_v3.0.2_with_ffmpeg_and_SimpleG.zip', 'wb') as f:
                f.write(zip)
        except Exception:
            print('下载器下载失败,请手动下载ZIP,并复制到此处')
            print(
                'https://github.com/nilaoda/N_m3u8DL-CLI/releases/download/3.0.2/N_m3u8DL-CLI_v3.0.2_with_ffmpeg_and_SimpleG.zip')
            input('操作完成后请回车')
        file = zipfile.ZipFile('N_m3u8DL-CLI_v3.0.2_with_ffmpeg_and_SimpleG.zip', 'r')
        file.extractall('./')
        file.close()
        os.remove('N_m3u8DL-CLI_v3.0.2_with_ffmpeg_and_SimpleG.zip')
        os.remove('N_m3u8DL-CLI-SimpleG.exe')
        print('下载器下载完成')

    for i in range(0, len(urls)):
        urls[i] = urls[i].replace('\n', '')
    dic = chuli(urls, names)
    download_dir = './Downloads/' + download_dir
    print('视频将保存到' + download_dir)
    threading.Thread(target=checkDone, args=(download_dir, len(urls))).start()
    for i in range(0, len(urls)):
        print('\r爬取进度:%d/%d' % (i + 1, len(urls)), end='')
        name = dic[urls[i].split('_')[1].split('.')[0]]
        # print(download_dir+'/'+name+'.mp4')
        if not os.path.exists(download_dir + '/' + str(i) + ' ' + name + '.mp4'):
            vbs = '''set ws=createobject("wscript.shell")
ws.run "1.bat",0
wscript.quit
            '''
            # 使用vbs调用bat,实现bat后台运行
            order = 'chcp 65001\nN_m3u8DL-CLI_v3.0.2.exe ' + urls[i] + ' --saveName "' + str(
                i) + ' ' + name + '" --enableDelAfterDone --workDir "' + download_dir + '"\nexit'
            with open('1.bat', 'w', encoding='utf-8') as f:
                f.write(order)
                f.close()
            with open('1.vbs', 'w') as f:
                f.write(vbs)
                f.close()
            os.system('start 1.vbs')
            sleep(waitForNewDownloadTime)
        else:
            print('\n' + download_dir + '/' + name + '.mp4' + ' 已存在，跳过')
    sleep(1.0)

def chuli(urls, names):
    dic = {}
    res = []
    for i in urls:
        i = i.split('_')[1].split('.')
        del i[-1]
        res.append(''.join(i))
    for i in range(0, len(res)):
        dic[res[i]] = names[i]
    return dic
