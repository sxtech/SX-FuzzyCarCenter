# -*- coding: cp936 -*-
import os
import sys
import glob
import time
import datetime
import MySQLdb
#import _mysql

def getTime():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

class FMysql:
    def __init__(self,host = 'localhost',user = 'root', passwd = '',ip='127.0.0.1'):
        self.host    = host
        self.user    = user
        self.passwd  = passwd
        self.port    = 3306
        self.db      = 'fuzzyq'
        self.charset = 'gbk'
        self.ip      = ip
        self.initime = None
        self.imgtime = None
        self.cur     = None
        self.conn    = None
        
    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()

    def login(self):
        try:
            self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,
                                        port=self.port,charset=self.charset,db=self.db)
            self.cur = self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        except Exception,e:
            raise

    def setupMysql(self):
        now = getTime()
        try:
            self.login()
        except Exception,e:
            print now,e
            print now,'Reconn after 15 seconds'
            time.sleep(15)
            self.setupMysql()
        else:
            pass
        
    def addHphm(self,values):
        try:
            self.cur.executemany("insert into platecode (p1,p2,p3,p4,p5,p6,p7,p8) values(%s,%s,%s,%s,%s,%s,%s,%s)",values)
            #s = self.cur.fetchall()
        except MySQLdb.Error,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    def setHphm(self,values):
        try:
            self.cur.executemany("insert into platecode (p1,p2,p3,p4,p5,p6,p7,p8) values(%s,%s,%s,%s,%s,%s,%s,%s)",values)
            self.cur.execute("SELECT LAST_INSERT_ID() as l_id")
        except MySQLdb.Error,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()
            return self.cur.fetchone()

##    def setTraffic(self,t1,t2,addr):
##        try:
##            print "insert into traffic (passtime,platecode_id,addr) values('%s','%s','%s')"%(t1,t2,addr)
##            self.cur.execute("insert into traffic (passtime,platecode_id,addr) values('%s','%s','%s')"%(t1,t2,addr))
##            self.cur.execute("SELECT LAST_INSERT_ID() as l_id")
##        except MySQLdb.Error,e:
##            self.conn.rollback()
##            raise
##        else:
##            self.conn.commit()
##            return self.cur.fetchone()


    def addTraffic(self,values):
        try:
            self.cur.executemany("insert into traffic (passtime,platecode_id) values(%s,%s)",values)
            #self.cur.execute("SELECT LAST_INSERT_ID()")
            #s = self.cur.fetchall()
        except MySQLdb.Error,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    def getTraffic(self,date,hphm_id):
        try:
            self.cur.execute("select * from traffic where platecode_id = %s and passtime = %s",(hphm_id,date))
            s = self.cur.fetchone()
        except MySQLdb.Error,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()
            return s

    def getHphm(self,hphm):
        try:
            self.cur.execute("select * from platecode where p1='%s'"%hphm)
            s = self.cur.fetchone()
        except MySQLdb.Error,e:
            #print e
            raise
        else:
            self.conn.commit()
            return s

    def getHphmInList(self,hphm=[]):
        try:
            print hphm
            strhphm = "','".join(hphm)
            self.cur.execute("select id,p1 from platecode where p1 in('%s')"%strhphm)
            s = self.cur.fetchall()
        except MySQLdb.Error,e:
            #print e
            raise
        else:
            self.conn.commit()
            return s


    def getTest(self):
        #print '123'
        self.cur.execute("select * from platecode where id = 481492")
        s = self.cur.fetchall()
        self.conn.commit()
        return s

        
    def endOfCur(self):
        self.conn.commit()
        
    def sqlCommit(self):
        self.conn.commit()
        
    def sqlRollback(self):
        self.conn.rollback()
            
if __name__ == "__main__":
    imgMysql = Mysql('localhost','root','','127.0.0.1')
    #address,passtime,hpzl,hphm,fxbh
    t1 = datetime.datetime(2014, 5, 18, 20, 20, 33)
    #new_time = datetime.datetime.now()
    imgMysql.login()

    s= imgMysql.getTest()
    print s
##    try:
        #print imgMysql.getTest()
        #imgMysql.addHphm([(u'粤B9041E'.encode('utf8'),'__','__','__','__','__','__','__'),])
##        a = imgMysql.getTest()
##        val = []
##        count = 0
##        for i in a:
##            if count >500:
##                break
##            val.append(i['p1'])
##            count += 1
##        strip = "','".join(val)
##        print strip
##    except Exception,e:
##        print e
        #print e[0]
    #print imgMysql.addTraffic2([(t1,23),(t1,21),(t1,22)])
    #print imgMysql.getHphmInList([u'粤LAG611'.encode('utf8'),u'粤BH9E39'.encode('utf8')])
    #print imgMysql.getHphm(u'粤LAG612'.encode('utf8'))
    #print imgMysql.getHbcByHphm(p1,new_time,u'粤L1234'.encode('utf8'))

    
    del imgMysql

