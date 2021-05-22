# 学习使用 Scrapy 的测试项目

学习 Scrapy 爬虫的第一个项目，目前编写的爬虫包括：

+ 个人博客文章爬虫
+ 豆瓣电影 TOP250 爬虫
+ 豆瓣读书 TOP250 爬虫
+ 豆瓣电影/读书 热门评论爬虫

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
在 Python 目录的 bin 文件夹内放入 Chromedriver，或放在喜欢的路径（已经放在爬虫项目根目录并配置）

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

### 🕷️ 豆瓣热门短评爬虫
热门短评在不登录情况下最多爬取220条，登录后最多爬取500条，由于热度动态改变，可能爬不满220或500（可能有重复）<br>

用户登录采用了手动登录，需要填写个人用户名和密码，运行爬虫时会弹出登录页面，手动拖动滑块完成登录验证<br>

豆瓣热门短评爬虫包括豆瓣电影和读书的热门短评爬取，为区分内容，为 spider 添加了两个参数，分别为评论类型和评论对象的ID，指令示例如下

```
# 豆瓣电影类型为 1
scrapy crawl comment -a douban_type=1 -a douban_id=1292052

# 豆瓣读书类型为 2
scrapy crawl comment -a douban_type=2 -a douban_id=6082808
```

## 数据查看
可使用 MongoDB Compass 查看及导出数据
![](https://cdn.jsdelivr.net/gh/kainzhang/kz-img/img/21/05/11/20210511103523.png)