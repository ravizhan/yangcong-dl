# yangcong-dl(https://github.com/ravizhan/yangcong-dl)
# Version 1.0.0

from flask import *
import webapi
import json
import os
import download

yangcong, dl_progress = None, 0

app = Flask(__name__)


@app.route('/')
def index():
    global yangcong
    if yangcong is not None and not yangcong.checkError()[1]:
        cs = yangcong.first_choose()
        return render_template("index.html", datas=cs[0], jsdatas=cs[1])
    else:
        if try_autologin():
            cs = yangcong.first_choose()
            return render_template("index.html", datas=cs[0], jsdatas=cs[1])
        return render_template("login.html")


@app.route("/loginget", methods=["GET"])
def login():
    global yangcong
    mode = request.values.get('mode')
    a = request.values.get("a")  # phone or code
    b = request.values.get("b")  # pswd
    save = request.values.get("save")  # pswd

    yangcong = webapi.YCForWeb(0, int(mode), a, b)
    if yangcong.checkError()[1]:
        return str(yangcong.checkError()[0])

    if save == 'true':
        yangcong.save_authorization()

    return 'YES'


@app.route("/logout", methods=["GET"])
def logout():
    global yangcong
    if yangcong:
        yangcong.delete_authorization()
        yangcong = None
    return 'OK'


def try_autologin():
    global yangcong
    if os.path.exists('authorization.txt'):
        yangcong = webapi.YCForWeb(startmode=1)
        return True
    else:
        return False


@app.route("/chs2", methods=["GET"])
def get2ndChs():
    subject_id = request.values.get("subject_id")
    stage_id = request.values.get("stage_id")
    publisher_id = request.values.get("publisher_id")
    semester_id = request.values.get("semester_id")
    chs2 = yangcong.second_choose(subject_id=subject_id, stage_id=stage_id, publisher_id=publisher_id,
                                  semester_id=semester_id)
    print(chs2)
    return jsonify(chs2[0])


@app.route("/untsclass", methods=["GET"])
def getUntsclass():
    global yangcong
    data = request.args.get('data')
    data = json.loads(data)
    _, topic_ids, name_list = yangcong.get_topic_and_name(data)
    print(name_list)
    return str(json.dumps([topic_ids, name_list]))


@app.route("/download", methods=["GET"])
def vd_downld():
    global yangcong, dl_progress
    dl_progress = 0
    data = request.args.get('data')
    data = json.loads(data)
    download_urls = yangcong.get_download_url(data[0])
    print(download_urls)
    download.download(download_urls, data[1], data[2], True)
    return 'ok'


@app.route("/progress", methods=["GET"])
def vd_downld_progress():
    global dl_progress
    return str(dl_progress)


@app.route("/progress_up", methods=["GET"])
def vd_downld_progress_up():
    global dl_progress
    dl_progress = int(str(request.values.get('data')))
    return 'ok'

@app.route('/video')
def vp():
    global yangcong
    if os.path.exists('templates/video.html'):
        if yangcong != None and yangcong.checkError()[1] == False:
            cs=yangcong.first_choose()
            return render_template("video.html",datas=cs[0],jsdatas=cs[1])
        else:
            if try_autologin():
                cs=yangcong.first_choose()
                return render_template("video.html",datas=cs[0],jsdatas=cs[1])
            return render_template("login.html")
    else:
        return '<h1>没有在templates文件夹下找到video.html插件。安装后方可使用。</h1>'


@app.route("/m3u8_url", methods=["GET"])
def m3u8_url():
    id = request.values.get("id")
    return yangcong.get_download_url( [id] )[0]


if __name__ == "__main__":
    print(
        '                 yangcong-dl\ngithub: https://github.com/ravizhan/yangcong-dl\nVersion 1.0.0     &  License： AGPL-3.0 license\n\n')
    app.run(port=5000, host="127.0.0.1")


