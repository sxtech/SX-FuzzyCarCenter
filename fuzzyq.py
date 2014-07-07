# -*- coding: cp936 -*-
import MySQLdb
from mysqldb import Mysql
from orcdb import Orc
from inicof import FuzzyQIni
import gl
import logging
import logging.handlers
import time,datetime,os,random,string

def getTime():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

class FuzzyQ:
    def __init__(self):
        self.fqIni = FuzzyQIni()
        mysqlset = self.fqIni.getMysqlConf()
        orcset   = self.fqIni.getOrcConf()
        systset  = self.fqIni.getSyst()
        
        self.mysqlHost = mysqlset['host']
        self.orcHost   = orcset['host']
        
        self.orc = Orc(orcset['host'],orcset['user'],orcset['passwd'],orcset['sid'])
        self.mysql = Mysql(mysqlset['host'],mysqlset['user'],mysqlset['passwd'])

        self.id_ = systset['cltxid']

        self.loginmysqlflag = True
        self.loginorcflag   = True

        logging.info('Logon System')
        

    def __del__(self):
        logging.info('Logout System')
        del self.orc
        del self.mysql
        del self.fqIni

    def longinMysql(self):
        try:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,getTime()+'Start to connect Mysql server '+self.mysqlHost))
            self.mysql.login()
            self.loginmysqlflag = False
        except Exception,e:
            self.loginmysqlflag = True
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,getTime()+str(e)))
            time.sleep(15)

    def loginOrc(self):
        try:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,getTime()+'Start to connect Oracle server '+self.mysqlHost))
            self.orc.login()
            self.loginorcflag = False
        except Exception,e:
            self.loginorcflag = True
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,getTime()+str(e)))
            time.sleep(15)

    #填充车牌号码     
    def decomposeHphm(self,hphm):
        if hphm == '':
            hphm = '-'
        pl = [hphm.encode('gbk')]
        hphm = hphm+'__________'
        for j in range(7):
            pl.append(hphm[j+1:j+3].encode('gbk'))
        return pl

    #添加车辆信息
    def addTraffic(self):
        values_2 = []
        hp_dict = {}
        hp_l = self.orc.getHphmByID(self.id_)
        if hp_l == []:
            time.sleep(1)
        else:
            for i in hp_l:
                try:
                    if i['HPHM'] != None and i['HPHM'] != '-':
                        now_date = datetime.date(i['JGSJ'].year,i['JGSJ'].month,i['JGSJ'].day)
                        hphm_obj = self.mysql.getHphm(i['HPHM'])
                        if hphm_obj == None:
                            values = []
                            u_hphm = i['HPHM'].decode('gbk','ignore')
                            values.append(self.decomposeHphm(u_hphm))
                            new_id = self.mysql.setHphm(values)['l_id']
                            #print new_id
                        else:
                            new_id = hphm_obj['id']

                        if self.mysql.getTraffic(now_date,new_id) == None and hp_dict.get(new_id,0)==0:
                            values_2.append((now_date,new_id))
                            hp_dict[new_id] = 1
                except MySQLdb.Error,e:
                    gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,getTime()+str(e)))
                    #print getTime(),e
                    if e[0] == 1267:
                        pass
                    else:
                        logging.error(str(e))
                        self.loginmysqlflag = True
                        return
                except Exception,e:
                    gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,getTime()+str(e)))
                    #print getTime(),e
                    if str(e)[:3] == 'ORA':
                        self.loginorcflag = True           
                        return
                    else:
                        logging.error(str(e))
                        pass
            try:
                if len(hp_l) < 20:
                    self.delFuzzyHphm()
                    time.sleep(1)

                self.mysql.addTraffic(values_2)
                self.id_ = hp_l[-1]['ID']
                self.fqIni.setSyst(self.id_)
                gl.TRIGGER.emit("<font %s>%s%s_%s</font>"%(gl.style_blue,getTime(),self.id_,hp_l[-1]['JGSJ']))
                #print getTime(),'done!',self.id_,hp_l[-1]['JGSJ']

            except MySQLdb.Error,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,getTime()+str(e)))
                #print getTime(),e
                if e[0] == 1267:
                    pass
                else:
                    logging.error(str(e))
                    self.loginmysqlflag = True
                    return
            except Exception,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,getTime()+str(e)))
                logging.error(str(e))
                if str(e)[:3] == 'ORA':
                    self.loginorcflag = True           
                    return
                else:
                    time.sleep(15)
                    pass

    def delFuzzyHphm(self):
        t1 = datetime.datetime.now()-datetime.timedelta(hours=2)
        ot_fuzzyid = self.orc.getOTFuzzyHphm(t1.strftime('%Y-%m-%d %H:%M:%S'))
        if ot_fuzzyid !=[]:
            self.orc.delFuzzyHphmByID(ot_fuzzyid[0][0])
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_orange,getTime()+'del '+str(ot_fuzzyid[0][0])))
            print getTime(),'del ',ot_fuzzyid[0][0]

    #主循环
    def mainLoop(self):
        while 1:
            if gl.QTFLAG == False:
                gl.DCFLAG = False
                break
            elif self.loginmysqlflag:
                self.longinMysql()
            elif self.loginorcflag:
                self.loginOrc()
            else:
                self.addTraffic()

if __name__ == "__main__":
    fq = FuzzyQ()
    fq.mainLoop()
    del fq








