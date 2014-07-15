# -*- coding: cp936 -*-
import MySQLdb
from mysqldb import FMysql
from orcdb import FOrc
from inicof import FuzzyQIni
from helpfunc import HelpFunc
import time,datetime,os,random,string
import logging
import logging.handlers
import gl

class FuzzyQ:
    def __init__(self):
        #�����ļ�
        self.fqIni = FuzzyQIni()
        mysqlset   = self.fqIni.getMysqlConf()
        orcset     = self.fqIni.getOrcConf()
        systset    = self.fqIni.getSyst()
        #����������
        self.hf  = HelpFunc()   

        #������IP
        self.mysqlHost = mysqlset['host']
        self.orcHost   = orcset['host']
        
        self.loginmysqlflag = False   #mysql ��¼���
        self.loginorcflag   = False   #oracle��¼���
        self.mysqlCount  = 0      #mysql ��¼����
        self.orcCount    = 0      #oracle��¼����
        
        #���ݿ�ʵ��
        self.mysql = FMysql(mysqlset['host'],mysqlset['user'],mysqlset['passwd'])
        self.orc = FOrc(orcset['host'],orcset['user'],orcset['passwd'],orcset['sid'])
        #��¼���ݿ�
        self.longinMysql()
        self.loginOrc()
        
        self.id_ = systset['cltxid']

        logging.info('Logon System')
        
    #��������
    def __del__(self):
        logging.info('Logout System')
        del self.orc
        del self.mysql
        del self.fqIni

    #mysql��¼
    def longinMysql(self):
        try:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Start to connect Mysql server '+self.mysqlHost))
            self.mysql.login()
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Login Mysql server success!'))
            self.loginmysqlflag = True
            self.mysqlCount = 0
        except Exception,e:
            self.loginmysqlflag = False
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
            self.mysqlCount = 1
            
    #oracle��¼
    def loginOrc(self):
        try:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Start to connect Oracle server '+self.orcHost))
            self.orc.login()
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Login Oracle server success!'))
            self.loginorcflag = True
            self.orcCount = 0
        except Exception,e:
            self.loginorcflag = False
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
            self.orcCount = 1

    #��䳵�ƺ���     
    def decomposeHphm(self,hphm):
        if hphm == '':
            hphm = '-'
        pl = [hphm.encode('gbk')]
        hphm = hphm+'__________'
        for j in range(7):
            pl.append(hphm[j+1:j+3].encode('gbk'))
        return pl

    #��ӳ�����Ϣ
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
                    gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                    logging.error(str(e))
                    if e[0] == 1267:
                        pass
                    else:
                        logging.error(str(e))
                        self.loginmysqlflag = False
                        return
                except Exception,e:
                    gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                    logging.error(str(e))
                    if str(e)[:3] == 'ORA':
                        self.loginorcflag = False           
                        return

            try:
                if len(hp_l) < 20:
                    self.delFuzzyHphm()

                self.mysql.addTraffic(values_2)
                self.id_ = hp_l[-1]['ID']
                self.fqIni.setSyst(self.id_)
                gl.TRIGGER.emit("<font %s>%s%s_%s</font>"%(gl.style_blue,self.hf.getTime(),self.id_,hp_l[-1]['JGSJ']))

            except MySQLdb.Error,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                if e[0] == 1267:
                    pass
                else:
                    logging.error(str(e))
                    self.loginmysqlflag = False
                    return
            except Exception,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                logging.error(str(e))
                if str(e)[:3] == 'ORA':
                    self.loginorcflag = False           
                    return
                else:
                    time.sleep(1)
                    pass

    #ɾ�����ڵ�fuzzy_id
    def delFuzzyHphm(self):
        t1 = datetime.datetime.now()-datetime.timedelta(hours=2)
        ot_fuzzyid = self.orc.getOTFuzzyHphm(t1.strftime('%Y-%m-%d %H:%M:%S'))
        if ot_fuzzyid !=[]:
            self.orc.delFuzzyHphmByID(ot_fuzzyid[0][0])
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_orange,self.hf.getTime()+'del '+str(ot_fuzzyid[0][0])))
            logging.warning('del '+str(ot_fuzzyid[0][0]))

    #��ѭ��
    def mainLoop(self):
        while 1:
            #�˳����
            if gl.QTFLAG == False:
                gl.DCFLAG = False
                break

            #��¼���
            if self.loginmysqlflag and self.loginorcflag:
                self.addTraffic()
            else:
                if not self.loginmysqlflag:
                    if self.mysqlCount > 15:
                        self.longinMysql()
                    else:
                        self.mysqlCount += 1

                if not self.loginorcflag:
                    if self.orcCount > 15:
                        self.loginOrc()
                    else:
                        self.orcCount += 1

            time.sleep(1)

if __name__ == "__main__":
    fq = FuzzyQ()
    fq.mainLoop()
    del fq








