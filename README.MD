##### 需求背景
> 得益于360加固的强大且免费，以及在Linux平台下良好的易用性，在过去的三年多时间里，一直在使用Jenkins自动化构建应用的同时进行应用加固，导致产生了3000多条加固记录。官网平台每一页只显示5条，而且不支持批量删除。如果需要手动删除这些记录，除了需要耐心，还需要花费大量的时间。

##### 注意事项
1. 由于需要实现的功能单一，没有必要实现自动登陆的功能
2. 使用之前需要先在网页端手动登陆后将cookie复制到脚本中

```python
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
```