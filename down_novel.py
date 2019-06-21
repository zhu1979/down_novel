#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @author: zhu1979
import os
import re
from random import choice
from time import sleep, time, strftime, localtime
from urllib import parse

from bs4 import BeautifulSoup
from requests import Session
from requests.adapters import HTTPAdapter
from tomorrow import threads

from getargs import _choose_args

count = 0
all_novel_renew = ''
renew_date = strftime('%Y%m%d', localtime())
renew_file = os.path.abspath('./novel/' + renew_date + '.txt')


def _set_dir():
    if not os.path.exists('./novel'):
        os.mkdir('./novel')


def _get_page(url, charset='utf-8'):
    """ 用于下载页面 """
    # nl = parse.urlsplit(url).netloc
    user_agents = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    ]
    user_agent = choice(user_agents)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "User-Agent": user_agent
    }
    # proxy = {'http': '127.0.0.1:1081'}
    # get时超时重试设置
    s = Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    r = s.get(url, headers=headers, allow_redirects=False, timeout=5)
    r.encoding = charset
    # r.encoding = r.apparent_encoding  # 较慢
    # soup = BeautifulSoup(r.text, 'html.parser')
    return r


@threads(80)
def _get_book_text(i, url, code, textcss):
    """ 按章节序号和url下载小说内容，写入以序号命名的txt文档 """
    global count, bookname, tmppath
    tmp = os.getcwd() + '/temp'
    if not os.path.exists(tmp):
        os.mkdir(tmp)
    tmppath = tmp + '/%s/' % bookname
    if not os.path.exists(tmppath):
        os.mkdir(tmppath)
    try:
        soup = BeautifulSoup(_get_page(url, charset=code).text, 'html.parser')
        # 获取章节标题
        chapter_title = soup.h1.contents[0]
        # 去除首尾空格
        chapter_title = chapter_title.strip()
        # 章节内容
        if parse.urlsplit(url).netloc == 'www.208xs.com':
            chapter_text = str(soup.select(textcss)[0])
            f_text = re.sub(r'</p><p>', '\n　　', chapter_text)
            f_text = re.sub(
                r'<div id="book_text"><p>|</p> <div id="ali"></div>\n</div>', '', f_text)
        else:
            chapter_text = soup.select(textcss)[0].text
            # 正则替换4个连续空格为换行和行首两个全角空格
            f_text = re.sub(r'\s{4,}|　{2}', '\n　　', chapter_text)
        # 在文件中写入章节标题和内容
        with open(tmppath + '%d.txt' % i, 'w', encoding='utf-8', errors='ignore') as f:
            f.write('## ' + chapter_title + '\n' + f_text + '\n\n')
        count += 1  # 下载章节数
    except AttributeError as e:
        print(url)
        print(e)


def _build_txt():
    """ 合并各章节文本文件 """
    global bookfile, count, chapter_count, bookname, tmppath, now_chapter_num
    old_file_size = os.path.getsize(bookfile) / float(1024 * 1024)
    wait_time = 1
    while True:
        if count < chapter_count:
            if wait_time < 120:
                sleep(2)
                wait_time += 1
                continue
            else:
                break
        elif count == chapter_count:
            novelfile = list(
                filter(lambda x: x[:x.index('.')].isdigit(),
                       os.listdir(tmppath)))
            novelfile.sort(key=lambda x: int(re.match(r'\d+', x).group()))
            txtfile_num = len(novelfile)
            string = ''
            if txtfile_num < count:
                sleep(2)
                continue
            elif txtfile_num == count:
                for dirFile in novelfile:
                    with open(tmppath + dirFile, 'r', encoding='utf-8', errors='ignore') as f:
                        string = string + '\n' + f.read()
                    os.remove(tmppath + dirFile)
                with open(bookfile, 'r', encoding='utf-8', errors='ignore') as of:
                    fline = int(re.sub(r'\n', '', of.readline()))
                    otext = of.read()
                with open(bookfile, 'w', encoding='utf-8', errors='ignore') as nf:
                    text = re.sub(r'\\xa0', '', string)
                    nf.write(str(now_chapter_num) + '\n' + otext + text)
        break

    if len(text) / float(1024 * 1024) < 1:
        renew = '# ' + bookname + '\n'
        with open(renew_file, 'a', encoding='utf-8', errors='ignore') as f:
            f.write(renew + text)

    print("%s 已下载 %d 章；" % (bookname, count))
    if old_file_size > 1:
        print("  原 %d 章，现 %d 章；" % (fline, now_chapter_num))
    else:
        print("  共 %d 章；" % (now_chapter_num))
    file_size = os.path.getsize(bookfile) / float(1024 * 1024)
    raise_size = file_size - old_file_size
    print('小说文件大小为：%.2f M, 新增：%.2f M。\n' % (file_size, raise_size))


def _get_book(url):
    """ 下载小说 """
    global bookfile, chapter_count, bookname, now_chapter_num
    code, booknamecss, authorcss, linkscss, textcss = _choose_args(url)
    try:
        soup = BeautifulSoup(_get_page(url, charset=code).text, 'html.parser')
        bookname = soup.select(booknamecss)[0].text
        bookname = re.sub(r'\n', '', bookname)
        bookname = re.sub(r'最新章节|更新列表|\s', '', bookname)
        author = soup.select(authorcss)[0].text
        author = re.sub(r'更新时间.*', '', author)
        author = re.sub(r'\s+', '', author)

        org_chapter_links = [parse.urljoin(url, chapter.get(
            'href')) for chapter in soup.select(linkscss)]
        org_chapter_links.reverse()  # 倒序排列
        chapter_links = list(set(org_chapter_links))  # 利用set去重
        chapter_links.sort(key=org_chapter_links.index)  # 根据之前倒序的index重新排序
        chapter_links.reverse()  # 倒序排列
        now_chapter_num = chapter_count = len(chapter_links)

        bookfile = './novel/%s.txt' % bookname
        # 新书或者是更新已下载的书
        if os.path.exists(bookfile):  # 更新
            with open(bookfile, 'r', encoding='utf-8', errors='ignore') as fo:
                first_line = fo.readline()
                old_chapter_count = int(re.sub(r'\n', '', first_line))
                chapter_num = chapter_count - old_chapter_count
                if chapter_num <= 0:
                    chapter_links = []
                    chapter_count = 0
                else:
                    chapter_links = chapter_links[-chapter_num:chapter_count]
                    chapter_count = chapter_num
        else:  # 新书
            with open(bookfile, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(str(len(chapter_links))+'\n\n' +
                        bookname + '\n' + author + '\n\n')
        if chapter_count == 0:
            print("%s 无更新！\n" % (bookname))
        else:
            print("%s 需下载 %d 章；" % (bookname, chapter_count))
        for i, url in enumerate(chapter_links):
            _get_book_text(i, url, code, textcss)
        if chapter_count > 0:
            _build_txt()
    except Exception as e:
        print(url, end='\n')
        print(e, end='\n')


def main():
    global count
    _set_dir()
    urls=['https://www.biquge.info/11_11656/']
    for url in urls:
        count = 0
        _get_book(url)


if __name__ == '__main__':
    t1 = time()
    main()
    t2 = time()
    print("下载更新总耗时：%.2f 秒。" % (t2 - t1))
    print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
