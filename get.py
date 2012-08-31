#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib
import urllib2
from BeautifulSoup import BeautifulSoup

def GetName(content):
    soup = BeautifulSoup(content)
    name = ' '
    for tmp in soup('title'):
        name = name + ' ' + unicode(tmp).encode("gbk")
    #print name
    name = name[name.find('>') + 1:]
    name = name[:name.find(' ')]
    #print name
    return name

def GetContent(url, proxy=1):
    if proxy:
        proxy_support = urllib2.ProxyHandler({'http':'http://10.155.168.250:8080'})
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    #print 'Get page: ' + url
    try:
        kidWeb = urllib2.urlopen(url)
        content = kidWeb.read().decode('gbk')
        kidWeb.close()
        return content
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason

def ParseUrl(content):
    pool = BeautifulSoup(content)
    target = ''

    results = pool.findAll(attrs={'align':'middle'})
    #print results
    for result in results:
        subUrl = ''
        for tmp in result.findAll('a', attrs={'href':True}):
            subUrl = subUrl + ' ' + unicode(tmp).encode("utf-8")

    subUrl = subUrl[subUrl.find('"') + 1:]
    subUrl = subUrl[:subUrl.find('"')]
    #print subUrl
    target = website + subUrl
    #print 'Target: ' + target 
    return target

def Download(url, name):
    localName = name + '.swf'
    print 'Trying to download file from [%s] and save as [%s]' % (url, localName)
    #req = urllib2.Request(url)
    #r = urllib2.urlopen(req)
    #f = open(localName, 'wb')
    #f.write(r.read())
    #f.close()
    #r.close()
    try :
        urllib.urlretrieve(url, localName)
    except Exception,e:
        print "Error: ",e

if __name__ == "__main__":
    website = 'http://www.520wawa.com'
    goPage = website + '/enfant/410/more_1.htm'
    content = GetContent(goPage)

    pool = BeautifulSoup(content)
    results = pool.body.findAll('li', attrs={'class' : 'article_text line'})
    subsite = ''

    for result in results:
        subsite = website + result.a['href']
        print subsite
        content = GetContent(subsite)
        #Get name
        fileName = GetName(content)
        #Get url
        url = ParseUrl(content)
        #Download file
        Download(url, fileName)

    print '\nFinished.'