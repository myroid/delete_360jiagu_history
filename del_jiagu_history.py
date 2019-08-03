#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import requests

del_app_url = 'http://jiagu.360.cn/web/apk/del'
app_list_url = 'http://jiagu.360.cn/web/apk/list'

total_count = 1
# 浏览器登录360加固平台，从控制台复制出cookies，填写到下面单引号中
cookies = dict(cookies_are='')


def del_app(app):
    params = {'apkMd5': app['apkMd5']}
    result = requests.get(del_app_url, cookies=cookies, params=params).json()
    name = app['name'].encode("utf-8")
    del_result = result['errMsg'] if result['errCode'] == 0 else result['data']
    print ('删除%s加固记录%s' % (name, del_result.encode("utf-8")))


def get_app_list():
    params = dict()
    params['limit'] = 1
    params['offset'] = 0
    params['name'] = ''
    params['fileName'] = ''
    return requests.get(app_list_url, cookies=cookies, params=params).json()


def del_jiagu_history():
    if not cookies['cookies_are']:
        print '请先在浏览器中登陆后复制cookie到字典中'
        sys.exit()

    global total_count
    while total_count > 0:
        result = get_app_list()
        if result['errCode'] == 0:
            total_count = result['data']['count']
            app_list = result['data']['list']
            for app in app_list:
                del_app(app)
        else:
            print result['errMsg']
    print 'Deleting completed'


del_jiagu_history()
