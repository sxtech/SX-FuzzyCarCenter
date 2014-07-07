# -*- coding: cp936 -*-
import cx_Oracle
import datetime

def getTime():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

class Orc:
    def __init__(self,host='localhost',user='fire', passwd='kakou',sid='ORCL'):
        self.host    = host
        self.user    = user
        self.passwd  = passwd
        self.port    = 1521
        self.sid     = sid
        self.cur = None
        self.conn = None
        
    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
        
    def login(self):
        try:
            self.conn = cx_Oracle.connect(self.user,self.passwd,self.host+':'+str(self.port)+'/'+self.sid)
            self.cur = self.conn.cursor()
            #print self.passwd
        except Exception,e:
            raise

    def setupOrc(self):
        import time
        try:
            self.login()
        except Exception,e:
            print now,e
            print now,'Reconn after 15 seconds'
            time.sleep(15)
            self.setupOrc()
        else:
            pass

    def getHphmByID(self,id_):
        try:
            self.cur.execute("select id,hphm,jgsj from cltx where id>%s and rownum<=100 order by id"%(id_))
        except Exception,e:
            raise
        else:
            return self.rowsToDictList()

    def getHphm(self,t1,t2):
        try:
            self.cur.execute("select distinct hphm from cltx where jgsj >= to_date('%s','yyyy-mm-dd hh24:mi:ss') and jgsj < to_date('%s','yyyy-mm-dd hh24:mi:ss')"%(t1,t2))
        except Exception,e:
            raise
        else:
            return self.rowsToDictList()

    def getHphm2(self,t1,t2):
        try:
            self.cur.execute("select hphm ,jgsj from cltx where jgsj >= to_date('%s','yyyy-mm-dd hh24:mi:ss') and jgsj < to_date('%s','yyyy-mm-dd hh24:mi:ss')"%(t1,t2))
        except Exception,e:
            raise
        else:
            return self.rowsToDictList()

    def getHphm3(self,t1,t2):
        try:
            self.cur.execute("select a.hphm,t.jgsj from (select distinct hphm from cltx where jgsj >= to_date('%s','yyyy-mm-dd hh24:mi:ss') and jgsj < to_date('%s','yyyy-mm-dd hh24:mi:ss'))a left join cltx t on a.hphm = t.hphm where t.jgsj >= to_date('%s','yyyy-mm-dd hh24:mi:ss') and jgsj < to_date('%s','yyyy-mm-dd hh24:mi:ss')"%(t1,t2,t1,t2))
        except Exception,e:
            raise
        else:
            return self.rowsToDictList()

    def getHphmByID(self,id_,rownum=100):
        try:
            self.cur.execute("select id,hphm,jgsj from cltx where id>'%s' and rownum<='%s'"%(id_,rownum))
        except Exception,e:
            raise
        else:
            #return self.cur.fetchall()
            return self.rowsToDictList()
        
    def getOTFuzzyHphm(self,t1):
        try:
            self.cur.execute("select id from fuzzy_hphm where timeflag<=to_date('%s','yyyy-mm-dd hh24:mi:ss') and flag=1"%t1)
            s = self.cur.fetchall()
            self.conn.commit()
        except Exception,e:
            raise
        else:
            return s

    def addFuzzy(self,time_,hphm):
        try:
            self.cur.execute("insert into fuzzy_hphm(TIMEFLAG,HPHM) values(to_date('%s','yyyy-mm-dd hh24:mi:ss'),'%s')"%(str(time_),hphm))
        except Exception,e:
            raise
        else:
            self.conn.commit()

    def delFuzzyHphmByID(self,id_):
        try:
            self.cur.execute("update fuzzy_hphm set flag=0 where id=%s"%id_)
            self.cur.execute("delete from hphm_list where fuzzy_id=%s"%id_)
        except Exception,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()
        
    def rowsToDictList(self):
        columns = [i[0] for i in self.cur.description]
        return [dict(zip(columns, row)) for row in self.cur]

    def orcCommit(self):
        self.conn.commit()

if __name__ == "__main__":
    
    orc = Orc()
    #values = []
    orc.setupOrc()
    #time = datetime.datetime(2013,3,3,01,01,01)
    #orc.addFuzzy(time,'粤L123%')
    s = orc.getOTFuzzyHphm('2012-05-01 1:19:47')
    print s
    for i in s:
        print i[0]
    #values = []
    #w_values=[]
    #while True:
        #print '2'
    #s=orc.getBkcp()
    #s = orc.rowsToDictList()
    #print s
    #time.sleep(3)
        #row_list = orc.rows_to_dict_list()
    #print len(row_list)
    #time = datetime.datetime(2013,3,3,01,01,01)
    #path = r'ImageFile\20130115\09\10.44.240.2\02\160001000.jpg'
    #print path
    #print path.decode('gbk')
    #w_values.append(('\xbd\xf8\xb3\xc7', '\xd4\xc1B1VC58', '', '\xc0\xb6\xc5\xc6', datetime.datetime(2014, 1, 13, 16, 58, 36), 14, '20140321\\12\\192.168.17.80\\1\\20140113165836670.jpg', 'SpreadDataG', '0', 'F', 'F', 'F', 'F', 'F', '\xc6\xbd\xcc\xb6\xce\xda\xcc\xc1\xbf\xa8\xbf\xda', 80, '1', '0', '1', '0', 0, '0'))
    #w_values.append(('\xbd\xf8\xb3\xc7','\xd4\xc1B1VC58', '', '\xc0\xb6\xc5\xc6', datetime.datetime(2014, 1, 13, 16, 58, 36), 14, '20140321\\12\\192.168.17.80\\1\\20140113165836670.jpg', 'SpreadDataG', '0', 'F', 'F', 'F', 'F','F', '\xc6\xbd\xcc\xb6\xce\xda\xcc\xc1\xbf\xa8\xbf\xda', 80, '1', '0', '1', '0', 0, '0'))
    #w_values.append(('\xbd\xf8\xb3\xc7','\xd4\xc1B1VC58','','\xc0\xb6\xc5\xc6',datetime.datetime(2014, 1, 13, 16, 58, 36),63,'20140321\\12\\192.168.17.80\\1\\20140113165836670.jpg','SpreadDataG','0','F','F','F','F','\xc6\xbd\xcc\xb6\xce\xda\xcc\xc1\xbf\xa8\xbf\xda',80,'1','0','1','123',23,'234'))
    #values.append(('进城','粤B','0','黄牌',time,45,'ImageFile\20130115\09\10.44.240.2\02\160001001.jpg'.decode('gbk').encode('gbk'),'SpreadDataG','0','T','F','F','F','测试卡口',80,'1','卡口编号','1','124',24,'235'))
    #print orc.getHphm('2013-01-01 00:00:00','2013-01-01 00:02:00')

##    strhphm = "','".join(s)
##    print strhphm
    del orc
    
    #orc.orcCommit()
    #orc.test()
