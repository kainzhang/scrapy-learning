# 学习使用 Scrapy 的测试项目

学习 Scrapy 爬虫的第一个项目，目前编写的爬虫包括：

+ 个人博客文章爬虫
+ 豆瓣电影 TOP250 爬虫

## 环境搭建
Python3, Scrapy, virtualenv(optional), MongoDB
```
pip3 install scrapy
```

创建项目（示例）
```
scrapy startproject douban
```

创建爬虫（示例）
```
cd douban
scrapy genspider movie movie.douban.com
```


## 运行流程
项目是用 PyCharm 创建的普通 Python项目，需要用终端运行，在根目录下先 cd 进入爬虫项目
```
cd douban
```
确保 MongoDB Server 开启，然后执行爬虫指令
```
scrapy crawl movie
```

## 查看数据
可使用 MongoDB Compass 查看及导出数据
![](https://cdn.jsdelivr.net/gh/kainzhang/kz-img/img/21/05/11/20210511103523.png)