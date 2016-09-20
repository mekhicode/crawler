# encoding: utf-8
import hashlib
import time
import urllib2

#请替换appkey和secret
appkey = "262585404"
secret = "471bd5d6ef3369a095f01e351fedd3b6"

paramMap = {
    "app_key": appkey,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")  #如果你的程序在国外，请进行时区处理
}
#排序
keys = paramMap.keys()
keys.sort()

codes= "%s%s%s" % (secret,str().join('%s%s' % (key, paramMap[key]) for key in keys),secret)

#计算签名
sign = hashlib.md5(codes).hexdigest().upper()

paramMap["sign"] = sign

#拼装请求头Proxy-Authorization的值
keys = paramMap.keys()
authHeader = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, paramMap[key]) for key in keys)

print authHeader

#接下来使用蚂蚁动态代理进行访问

proxy_handler = urllib2.ProxyHandler({"http": 'http://test.proxy.mayidaili.com:8123'})
opener = urllib2.build_opener(proxy_handler)

request = urllib2.Request('http://1212.ip138.com/ic.asp')

# 将authHeader放入请求头中即可,注意authHeader必须在每次请求时都重新计算，要不然会因为时间误差而认证失败
request.add_header('Proxy-Authorization', authHeader)

response = opener.open(request)

print response.read()
