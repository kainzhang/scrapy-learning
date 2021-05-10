# 学习使用 Scrapy 的测试项目

学习 Scrapy 爬虫的第一个项目，爬了自己的博客 lokka.me

## 环境搭建
Python3, Scrapy, virtualenv(optional), MongoDB
```
pip3 install scrapy
```

创建项目（已经创建）
```
scrapy startproject lokka
```

创建爬虫（已经创建）
```
scrapy genspider lokkame lokka.me
```


## 运行流程
项目是用 PyCharm 创建的普通 Python项目，需要用终端运行，在根目录下先 cd 进入爬虫项目
```
cd lokka
```
确保 MongoDB Server 开启，然后执行爬虫指令
```
scrapy crawl lokkame
```

## 查看数据
终端或者 MongoDB Compass 查看数据
![](https://cdn.jsdelivr.net/gh/kainzhang/kz-img/img/21/05/10/20210510134419.png)