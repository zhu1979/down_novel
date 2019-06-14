#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from urllib import parse


def _choose_args(url):
    """ 按照url地址信息确定CSS获取器内容 """
    # base = parse.urlsplit(url).scheme
    nl = parse.urlsplit(url).netloc
    gbklist = [
        'www.biquyun.com',
        'www.biquge.cm',
        'www.x88dushu.com',
        'www.ddxs.cc',
        'www.23us.net',
        'www.biqugex.com',
        'www.xbequge.com',
        'www.biqiku.com',
        'www.biquxu.com',
        'www.x23us.com',
        'www.23wx.cc',
        'www.bequge.com',
    ]
    bqglist = [
        'www.biquyun.com',
        'www.biquge.cm',
        'www.xbiquge6.com',
        'www.biquge.info',
        'www.biquke.com',
        'www.ddxs.cc',
        'www.xbiquge6.com',
        'www.biqiku.com',
        'www.biqudao.com',
        'www.biquku.co',
        'www.23wx.cc',
        'www.dingdiann.com',
        'www.bequge.com',
    ]
    if nl in bqglist:
        booknamecss = 'div#info > h1'
        authorcss = 'div#info > p:nth-of-type(1)'
        linkscss = 'dd > a'
        textcss = 'div#content'
    elif nl == 'www.x88dushu.com':
        booknamecss = 'div.rt > h1'
        authorcss = 'div.msg > em:nth-of-type(1)'
        linkscss = 'div.mulu > ul > li > a'
        textcss = 'div.yd_text2'
    elif nl == 'www.23us.so' or nl == 'www.x23us.com':
        booknamecss = 'dl > dd > h1'
        authorcss = 'dl > dd > h3:nth-of-type(1)'
        linkscss = 'td.L > a'
        textcss = 'dd#contents'
    elif nl == 'www.23us.net':
        booknamecss = 'div.btitle > h1'
        authorcss = 'div.btitle > em'
        linkscss = 'dd > a'
        textcss = 'div#BookText'
    elif nl == 'www.biqugex.com':
        booknamecss = 'div.info > h2'
        authorcss = 'div.small > span:nth-of-type(1)'
        linkscss = ' dd > a'
        textcss = 'div#content'
    elif nl == 'www.xbequge.com' or nl=='www.biquxu.com':
        booknamecss = 'div.info > h1'
        authorcss = 'div.info > h3'
        linkscss = 'ul#chapterlist > li > a'
        textcss = 'div#book_text'
    elif nl == 'www.208xs.com':
        booknamecss = 'div.info > h1'
        authorcss = 'div.info > h3'
        linkscss = 'div.article_texttitleb > ul > li > a'
        textcss = 'div#book_text'
    if nl in gbklist:
        code = 'gbk'
    else:
        code = 'utf-8'
    return code, booknamecss, authorcss, linkscss, textcss
