# -*- coding: cp936 -*-
import time
import datetime
import MySQLdb

class FCMysql:
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

    #批量添加车牌
    def addHphm(self,values):
        try:
            self.cur.executemany("insert into platecode (p1,p2,p3,p4,p5,p6,p7,p8) values(%s,%s,%s,%s,%s,%s,%s,%s)",values)
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

    #批量添加车流信息
    def addTraffic(self,values):
        try:
            self.cur.executemany("insert into traffic (passtime,platecode_id) values(%s,%s)",values)
        except MySQLdb.Error,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    #查询车流信息
    def getTraffic(self,date,hphm_id):
        try:
            self.cur.execute("select * from traffic where platecode_id = %s and passtime = '%s'"%(hphm_id,date))
            s = self.cur.fetchone()
        except MySQLdb.Error,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()
            return s

    #根据车牌号查询platecode
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
            raise
        else:
            self.conn.commit()
            return s


    def getPlatecode(self,_id=1,offset=10000):
        self.cur.execute("select id,p1 from platecode where id>%s and id<=%s"%(_id,_id+offset))
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
    imgMysql = FCMysql('localhost','root','','127.0.0.1')
    #address,passtime,hpzl,hphm,fxbh
    #values = [('\xd4\xc1LKL088', 'LK', 'KL', 'L0', '08', '88', '8_', '__'),
              #('\xd4\xc1LHN503', 'LH', 'HN', 'N5', '50', '03', '3_', '__'),
              #('\xd4\xc1LNJ799', 'LN', 'NJ', 'J7', '79', '99', '9_', '__')]
    #values = [('\xd4\xc1LHN503', 'LH', 'HN', 'N5', '50', '03', '3_', '__'),('\xd4\xc1LNJ799', 'LN', 'NJ', 'J7', '79', '99', '9_', '__')]
    #new_time = datetime.datetime.now()
    values = [(datetime.date(2013, 1, 3), 164276), (datetime.date(2013, 1, 3), 164277), (datetime.date(2013, 1, 3), 164278), (datetime.date(2013, 1, 3), 122461), (datetime.date(2013, 1, 3), 12429), (datetime.date(2013, 1, 3), 457), (datetime.date(2013, 1, 3), 164279), (datetime.date(2013, 1, 3), 24862), (datetime.date(2013, 1, 3), 98916), (datetime.date(2013, 1, 3), 164280), (datetime.date(2013, 1, 3), 34535), (datetime.date(2013, 1, 3), 16057), (datetime.date(2013, 1, 3), 164281), (datetime.date(2013, 1, 3), 164282), (datetime.date(2013, 1, 3), 20225), (datetime.date(2013, 1, 3), 57961), (datetime.date(2013, 1, 3), 164283), (datetime.date(2013, 1, 3), 134764), (datetime.date(2013, 1, 3), 96959), (datetime.date(2013, 1, 3), 164284), (datetime.date(2013, 1, 3), 164285), (datetime.date(2013, 1, 3), 56817), (datetime.date(2013, 1, 3), 35130), (datetime.date(2013, 1, 3), 3177), (datetime.date(2013, 1, 3), 164286), (datetime.date(2013, 1, 3), 164284), (datetime.date(2013, 1, 3), 164287), (datetime.date(2013, 1, 3), 55138), (datetime.date(2013, 1, 3), 25072), (datetime.date(2013, 1, 3), 13196), (datetime.date(2013, 1, 3), 164288), (datetime.date(2013, 1, 3), 53825), (datetime.date(2013, 1, 3), 26658), (datetime.date(2013, 1, 3), 164289), (datetime.date(2013, 1, 3), 9788), (datetime.date(2013, 1, 3), 164290), (datetime.date(2013, 1, 3), 164291), (datetime.date(2013, 1, 3), 164292), (datetime.date(2013, 1, 3), 164293), (datetime.date(2013, 1, 3), 124790), (datetime.date(2013, 1, 3), 164294), (datetime.date(2013, 1, 3), 140443), (datetime.date(2013, 1, 3), 91699), (datetime.date(2013, 1, 3), 164295), (datetime.date(2013, 1, 3), 38119), (datetime.date(2013, 1, 3), 31732), (datetime.date(2013, 1, 3), 24391), (datetime.date(2013, 1, 3), 164296), (datetime.date(2013, 1, 3), 164297), (datetime.date(2013, 1, 3), 164298), (datetime.date(2013, 1, 3), 164299)]
    values2 = [(datetime.date(2013, 1, 3), 164276), (datetime.date(2013, 1, 3), 164277), (datetime.date(2013, 1, 3), 164278), (datetime.date(2013, 1, 3), 122461), (datetime.date(2013, 1, 3), 12429), (datetime.date(2013, 1, 3), 457), (datetime.date(2013, 1, 3), 164279), (datetime.date(2013, 1, 3), 24862), (datetime.date(2013, 1, 3), 98916), (datetime.date(2013, 1, 3), 164280), (datetime.date(2013, 1, 3), 34535), (datetime.date(2013, 1, 3), 16057), (datetime.date(2013, 1, 3), 164281), (datetime.date(2013, 1, 3), 164282), (datetime.date(2013, 1, 3), 20225), (datetime.date(2013, 1, 3), 57961), (datetime.date(2013, 1, 3), 164283), (datetime.date(2013, 1, 3), 134764), (datetime.date(2013, 1, 3), 96959), (datetime.date(2013, 1, 3), 164284), (datetime.date(2013, 1, 3), 164285), (datetime.date(2013, 1, 3), 56817), (datetime.date(2013, 1, 3), 35130), (datetime.date(2013, 1, 3), 3177), (datetime.date(2013, 1, 3), 164286)]
    values3 = [(datetime.date(2013, 1, 3), 164284), (datetime.date(2013, 1, 3), 164287), (datetime.date(2013, 1, 3), 55138), (datetime.date(2013, 1, 3), 25072), (datetime.date(2013, 1, 3), 13196), (datetime.date(2013, 1, 3), 164288), (datetime.date(2013, 1, 3), 53825), (datetime.date(2013, 1, 3), 26658), (datetime.date(2013, 1, 3), 164289), (datetime.date(2013, 1, 3), 9788), (datetime.date(2013, 1, 3), 164290), (datetime.date(2013, 1, 3), 164291), (datetime.date(2013, 1, 3), 164292), (datetime.date(2013, 1, 3), 164293), (datetime.date(2013, 1, 3), 124790), (datetime.date(2013, 1, 3), 164294), (datetime.date(2013, 1, 3), 140443), (datetime.date(2013, 1, 3), 91699), (datetime.date(2013, 1, 3), 164295), (datetime.date(2013, 1, 3), 38119), (datetime.date(2013, 1, 3), 31732), (datetime.date(2013, 1, 3), 24391), (datetime.date(2013, 1, 3), 164296), (datetime.date(2013, 1, 3), 164297), (datetime.date(2013, 1, 3), 164298), (datetime.date(2013, 1, 3), 164299)]
    imgMysql.login()
    print imgMysql.getHphm('\xe7\xb2\xa4L88888')
    #imgMysql.addTraffic(values3)
    
    del imgMysql

