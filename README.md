# Crawl_Novel

一个简陋的小说下载器；

## 可以自行修改增加小说网站

在`getargs.py`文件中，按照我的格式添加如下内容的CSS选择器：
- 小说名
- 作者
- 章节目录
- 章节内容
- 页面编码

## 需要安装的模块

- BeautifulSoup
- tomorrow

  这个模块最好稍微修改一下20和42行的`async`，可能会和`asyncio`有点冲突。