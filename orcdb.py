# -*- coding: cp936 -*-
import cx_Oracle
import datetime

class FOrc:
    def __init__(self,host='localhost',user='fire', passwd='kakou',sid='ORCL'):
        self.host   = host
        self.user   = user
        self.passwd = passwd
        self.port   = 1521
        self.sid    = sid
        self.cur    = None
        self.conn   = None
        
    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
        
    def login(self):
        try:
            self.conn = cx_Oracle.connect(self.user,self.passwd,self.host+':'+str(self.port)+'/'+self.sid)                       
            self.cur = self.conn.cursor()
        except Exception,e:
            raise

    def getHphmByID2(self,id_):
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

    #根据ID查询车牌信息
    def getHphmByID(self,id_,rownum=1000):
        try:
            self.cur.execute("select id,hphm,jgsj from cltx where id>'%s' and id<='%s' order by id"%(id_,id_+rownum))
        except Exception,e:
            raise
        else:
            return self.rowsToDictList()

    #根据时间查询模糊车牌
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

    #根据ID删除模糊车牌号
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

    orc.login()

    s = orc.getOTFuzzyHphm('2012-05-01 1:19:47')
    print s
    for i in s:
        print i[0]

    del orc

