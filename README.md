# 学习使用 Scrapy 的测试项目

学习 Scrapy 爬虫的第一个项目，目前编写的爬虫包括：

+ 个人博客文章爬虫
+ 豆瓣电影 TOP250 爬虫
+ 豆瓣读书 TOP250 爬虫

## 环境搭建

### 主要依赖
+ Python3
+ Scrapy
+ Selenium

### 数据库
+ MongoDB

### 安装依赖
```
pip3 install scrapy
pip3 install selenium
```

## 运行流程

创建项目（示例）
```
scrapy startproject douban
```

创建爬虫（示例）
```
cd douban
scrapy genspider movie movie.douban.com
```

项目是用 PyCharm 创建的普通 Python项目，需要用终端运行，在根目录下先 cd 进入爬虫项目
```
cd douban
```
确保 MongoDB Server 开启，然后执行爬虫指令
```
scrapy crawl movie
```

## 数据查看
可使用 MongoDB Compass 查看及导出数据
![](https://cdn.jsdelivr.net/gh/kainzhang/kz-img/img/21/05/11/20210511103523.png)