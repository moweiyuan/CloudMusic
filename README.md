# 网易云音乐热门歌单可视化大屏

- CloudMusic里为第一个大屏项目
- Spider里为爬虫文件
- Data里为歌单数据文件

安装好需要的python库，将cloudmusic.sql导入mysql数据库，在命令行执行python app.py，在浏览器打开http://127.0.0.1:5000 即可。


爬虫部分需要先装好python文件所导入的第三方库，先在mysql数据库中建好表。如果不想建表可以在mysql中建一个同名的cloudmusic数据库，将cloudmusic.sql导入，再delete from playlists删除表中数据，就可得到一个无数据的表结构。

playlists表字段信息：
https://github.com/moweiyuan/CloudMusic/blob/master/Data/%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E7%BB%93%E6%9E%84.png?raw=true
