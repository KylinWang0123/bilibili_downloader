#encoding:utf-8
"""
脚本目标：爬去目标B站网页的视频，需要安装ffmpeg-python功能包
具体过程为(默认仅下载当前网页视频)：
    1. 仅下载当前视频: python3 BDownloader.py -single True -url https://www.bilibili.com/video/BV1Ci4y1L7ZZ?p=1
    2. 下载右侧列表中所有的视频: python3 BDownloader.py -single False -url https://www.bilibili.com/video/BV1Ci4y1L7ZZ?p=1
    PS: 下载所有视频的过程为，先下载所有视频的mp3和mp4到文件夹，再进行进一步合成，合成过程比较花费时间，并且存储空间要足够
"""

import sys
import requests
import os
import json
import re
import ffmpeg
import time



# 下载功能实现
def download(link, link_headers, save_title):
    print("Downloading Video from " + link)
    response = requests.get(link, headers=link_headers)
    html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', response.text)[0]  # 网址数据
    json_data = json.loads(html_data)  # Json化
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']  # 音频地址
    video_url = json_data['data']['dash']['video'][0]['baseUrl']  # 视频地址
    audio_content = requests.get(url=audio_url, headers=headers).content  # 获取音频
    video_content = requests.get(url=video_url, headers=headers).content  # 获取视频
    with open("./TMP_STORE/" + save_title + ".mp4", mode="wb") as f:  # 保存视频
        f.write(video_content)
    with open("./TMP_STORE/" + save_title + ".mp3", mode="wb") as f:  # 保存音频
        f.write(audio_content)
    response.close()
# 转换功能实现
def mergeSound2Mp4(sndName, vidName, saveName):
    video = ffmpeg.input(vidName)
    sound = ffmpeg.input(sndName)
    ffmpeg.concat(video, sound, v=1, a=1).output(saveName).run()

downLoadSingle = True
url_source = ""
# 只是伪装
headers = {"referer": "https://www.bilibili.com/",  # 告诉服务器，当前网址是从这个网址条转过来
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}




if __name__ == "__main__":
    # 解析参数
    if len(sys.argv) < 3:
        print("参数数量错误")
        sys.exit()
    elif len(sys.argv) == 3:
        if "-url" not in sys.argv:
            print("没有指定url参数，请按照python3 BDownloader.py -url 网址")
            sys.exit()
    elif len(sys.argv) == 5:
        if "-single" and "-url" not in sys.argv:
            print("正确输入为：python3 BDownloader.py -single True/False -url 网址")
            sys.exit()
        else:
            sIndex = sys.argv.index("-single")
            urlIndex = sys.argv.index("-url")
            param_1 = sys.argv[sIndex+1]
            param_2 = sys.argv[urlIndex+1]
            if param_1 == "True":
                downLoadSingle = True
            elif param_1 == "False":
                downLoadSingle = False
            else:
                print("-single对应的输入参数错误")
                sys.exit()
            url_source = sys.argv[urlIndex+1]

    # 尝试打开网址
    response = requests.get(url_source, headers=headers)
    if response.status_code != 200:
        print("打开网页错误，请检查网址")
    else:
        print("网页获取成功，正在解析网页")
    # 解析网页
    singgle_title = re.findall('h1 title="(.*?)" class="video-title"',response.text)[0]
    titles = re.findall('"from":"vupload","part":"(.*?)","duration"', response.text)    # 解析列表中所有的视频
    response.close()    # 暂且关闭当前网页
    vid_cnt = len(titles)
    urls = []
    for i in range(vid_cnt):    # 列表中所有的下载用url
        j = i+1
        urls.append(url_source+"?p="+str(j))

    # 判断下载当前还是所有的视频
    os.system("rm -rf TMP_STORE")
    os.system("mkdir TMP_STORE")
    if downLoadSingle ==  True:     #只下载一个
        retryFlag = True
        retryCnt = 1
        while(retryFlag):
            try:
                download(link=url_source, link_headers=headers, save_title=singgle_title)
                retryFlag = False
            except Exception as e:
                print("Retry Download " + url_source + " #" + str(retryCnt))
                retryCnt = retryCnt + 1
    else:
        for (title, url_link) in zip(titles, urls):
            retryFlag = True
            retryCnt = 1
            while(retryFlag):
                try:
                    download(link=url_link, link_headers=headers, save_title=title)
                    retryFlag = False
                except Exception as e:
                    print("Retry Download " + url_link + " #" + str(retryCnt))
                    retryCnt = retryCnt + 1
    # 完成下载后进行转换，转换后放入 videos 文件夹下
    os.system("rm -rf Videos")
    os.system("mkdir Videos")
    time.sleep(2)
    if downLoadSingle == True:
        vidName = "./TMP_STORE/" + singgle_title + ".mp4"
        sndname = "./TMP_STORE/" + singgle_title + ".mp3"
        saveName = "./Videos/" + singgle_title + ".mp4"
        mergeSound2Mp4(sndname, vidName, saveName)
    else:
        for title in titles:
            vidName = "./TMP_STORE/" + title + ".mp4"
            sndName = "./TMP_STORE/" + title + ".mp3"
            saveName = "./Video/" + title + ".mp4"
            mergeSound2Mp4(sndName, vidName, saveName)
    # 全部转换完毕
    os.system("rm -rf TMP_STORE")












