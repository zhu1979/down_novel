#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
#
import os
import re
from time import localtime, sleep, strftime, time
from urllib import parse

from bs4 import BeautifulSoup
from tomorrow import threads

from downpage import _get_page
from getargs import _choose_args
from setdir import _set_dir

count = 0
all_novel_renew = ''
renew_date = strftime('%Y%m%d', localtime())
renew_file = os.path.abspath('./novel/' + renew_date + '.txt')


@threads(80)
def _get_book_text(i, url, code, textcss):
    """ 按章节序号和url下载小说内容，写入以序号命名的txt文档 """
    global count, bookname, tmppath
    tmp = os.getcwd() + '/temp'
    _set_dir(tmp)
    tmppath = tmp + '/%s/' % bookname
    _set_dir(tmppath)
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
        f_text = re.sub(
            r'笔.趣.阁[wｗ].*[fｆ][oｏ]|.*chaptererror.*|正在手打中.*|\u3000{2}灯笔.*| \
            \u3000{2}P[sS][:：].*|app2\(\);|\u3000{2}\(http.*|\u3000{2}请记住本书首发域名.*| \
            【笔.趣.阁.*[bｂBＢ]iz】|一秒记住.*|[7７七⑦][8８八⑧]中文.*|七\^八中文.*|　　</div>| \
            　　【.*换源app.*】\n|　　【.*野果阅读.*】\n', '',
            f_text)
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
                f.write(str(len(chapter_links)) + '\n\n' +
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
    _set_dir('./novel')
    urls = ['https://www.biquge.info/11_11656/']
    for url in urls:
        count = 0
        _get_book(url)


if __name__ == '__main__':
    t1 = time()
    main()
    t2 = time()
    print("下载更新总耗时：%.2f 秒。" % (t2 - t1))
    print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
