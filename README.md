# 网易云音乐热门歌单可视化大屏

11.28更新：
CloudMusic02中的文件无须使用Python和MySQL，点击index.html即可打开看到效果。

-------------------------------------------------------------------------

- CloudMusic里为第一个大屏项目
- Spider里为爬虫文件
- Data里为歌单数据文件

安装好需要的python库，将cloudmusic.sql导入mysql数据库，在命令行执行python app.py，在浏览器打开http://127.0.0.1:5000 即可。


运行爬虫部分需要先装好python文件所导入的第三方库，先在mysql数据库中建好表。如果不想建表可以在mysql中建一个同名的cloudmusic数据库，将cloudmusic.sql导入，再delete from playlists删除表中数据，就可得到一个无数据的表结构。之后打开命令行，运行python playlist.py即可。

playlists表字段信息：
https://github.com/moweiyuan/CloudMusic/blob/master/Data/%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E7%BB%93%E6%9E%84.png?raw=true

爬虫运行截图：
https://github.com/moweiyuan/CloudMusic/blob/master/Spider/%E7%88%AC%E8%99%AB%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE.png?raw=true
