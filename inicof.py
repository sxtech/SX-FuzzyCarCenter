#-*- encoding: gb2312 -*-
import ConfigParser
import string, os, sys
import datetime
import time


class FuzzyQIni:
    def __init__(self,confpath = 'fuzzyq.conf'):
        self.confpath = confpath
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)

    def getSyst(self):
        cf = ConfigParser.ConfigParser()
        syst = {}
        syst['cltxid'] = self.cf.getint('SYST','cltxid')
        return syst

    def setSyst(self,cltxid):
        self.cf.set('SYST', 'cltxid', cltxid)
        fh = open(self.confpath, 'w')
        self.cf.write(fh)
        fh.close()
    
    def getOrcConf(self):
        orcconf = {}
        orcconf['host']   = self.cf.get('ORCSET','host')
        orcconf['user']   = self.cf.get('ORCSET','user')
        orcconf['passwd'] = self.cf.get('ORCSET','passwd')
        orcconf['port']   = self.cf.get('ORCSET','port')
        orcconf['sid']    = self.cf.get('ORCSET','sid')
        return orcconf

    def getMysqlConf(self):
        mysqlconf = {}
        mysqlconf['host']    = self.cf.get('MYSQLSET','host')
        mysqlconf['user']    = self.cf.get('MYSQLSET','user')
        mysqlconf['passwd']  = self.cf.get('MYSQLSET','passwd')
        mysqlconf['port']    = self.cf.getint('MYSQLSET','port')
        mysqlconf['db']      = self.cf.get('MYSQLSET','db')
        mysqlconf['charset'] = self.cf.get('MYSQLSET','charset')
        return mysqlconf
     
if __name__ == "__main__":
    #PATH = 'F:/卡口/imgs/ImageFile/平潭乌塘卡口/20140304/11/1(出城)/20140113164737680_蓝牌粤B9041J.ini'
    PATH2 = 'F:\\卡口\\imgs\\ImageFile\\平潭乌塘卡口\\20140304\\11\\1(出城)\\20140113164737680_蓝牌粤B9041J.ini'
    #PATH3 = 'F:\卡口\imgs\ImageFile\平潭乌塘卡口\20140304\11\test\20140113164940250_蓝牌粤LF2473.ini'
##    print "r'"+PATH2+"'"
    try:
        fq = FuzzyQIni()
        #fq.getOrcConf()
        print fq.setSyst(1234)
        #s = imgIni.getPlateInfo(PATH2)
        #i = s['host'].split(',')
        #print s
        #disk = s['disk'].split(',')
        #print disk
        #del i
    except ConfigParser.NoOptionError,e:
        print e
        time.sleep(10)
    #print s['path']

#print cf.sections()
#s = cf.get('')
