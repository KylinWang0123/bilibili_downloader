# bilibili_downloader

# 用于下载B站视频的爬虫脚本，依赖ffmpeg-python

-single True: 下载当前页面
-single False: 批量下载右侧列表内所有视频
使用范例：

python3 BDownloader.py -single True -url https://www.bilibili.com/video/BV1Ci4y1L7ZZ

下载后为无声mp4和mp3文件，存储在当前文件夹下的TMP_STORE文件夹。 进一步使用了ffmpeg转换到Videos文件夹下，完成所有转换后TMP_STORE文件夹被删除。
