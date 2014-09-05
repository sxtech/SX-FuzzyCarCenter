# -*- coding: cp936 -*-
import MySQLdb
from mysqldb import FCMysql
from orcdb import FOrc
from inicof import FuzzyQIni
from helpfunc import HelpFunc
import time,datetime,os,random,string
import logging
import gl

logger = logging.getLogger('root')

class FuzzyQ:
    def __init__(self):
        #配置文件
        self.fqIni = FuzzyQIni()
        mysqlset   = self.fqIni.getMysqlConf()
        orcset     = self.fqIni.getOrcConf()
        systset    = self.fqIni.getSyst()
        #辅助函数类
        self.hf  = HelpFunc()   

        #服务器IP
        self.mysqlHost = mysqlset['host']
        self.orcHost   = orcset['host']
        
        self.loginmysqlflag = False   #mysql 登录标记
        self.loginorcflag   = False   #oracle登录标记
        self.mysqlCount = 0      #mysql 登录计数
        self.orcCount   = 0      #oracle登录计数
        
        #数据库实例
        self.mysql = FCMysql(mysqlset['host'],mysqlset['user'],mysqlset['passwd'])
        self.orc = FOrc(orcset['host'],orcset['user'],orcset['passwd'],orcset['sid'])
        #登录数据库
        self.longinMysql()
        self.loginOrc()
        
        self.id_ = systset['cltxid']

        self.hphm_dict = {}            #车牌号码字典
        self.hphmdictflag = False      #初始化车牌字典标记
        self.invalidhphm = -1

    #mysql登录
    def longinMysql(self):
        try:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Start to connect Mysql server '+self.mysqlHost))
            self.mysql.login()
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Login Mysql server success!'))
            self.loginmysqlflag = True
            self.mysqlCount = 0
        except Exception,e:
            self.loginmysqlflag = False
            self.mysqlCount = 1
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
            
    #oracle登录
    def loginOrc(self):
        try:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Start to connect Oracle server '+self.orcHost))
            self.orc.login()
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Login Oracle server success!'))
            self.loginorcflag = True
            self.orcCount = 0
        except Exception,e:
            self.loginorcflag = False
            self.orcCount = 1
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))

    #车牌号码分解
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
        traffic_set = set()  #traffic表数据
        miss_hphm = set()    #未缓存的车牌号码
        hphm_list = []

        #从oracle获取车牌号和时间
        try:
            hp_l = self.orc.getHphmByID(self.id_,1000)
        except Exception,e:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
            logger.error(str(e))
            self.loginorcflag = False
            self.orcCount = 0
            return
        
        if hp_l == []:
            try:
                self.delFuzzyHphm()
                time.sleep(1)
            except Exception,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                logger.error(str(e))
                self.loginorcflag = False
                self.orcCount = 0
                return       
        else:
            try:
                #检查platecode表是否有车牌号
                for i in hp_l:
                    if i['HPHM'] != None and i['HPHM'] != '-':
                        hphm_id = self.hphm_dict.get(i['HPHM'],-1)
                        if hphm_id == -1:
                            if i['HPHM'] in miss_hphm:
                                pass
                            else:
                                miss_hphm.add(i['HPHM'])
                                hphm_list.append(tuple(self.decomposeHphm(i['HPHM'].decode('gbk','ignore'))))
                if hphm_list != []:
                    self.mysql.addHphm(hphm_list)   #添加车牌号码到platecode表
                
                #添加新的车牌号到缓存
                for i in miss_hphm:
                    hphmobj = self.mysql.getHphm(i)
                    if hphmobj != None:
                        self.hphm_dict[i] = hphmobj['id']

                #检查traffic表是否有车牌号
                for i in hp_l:
                    if i['HPHM'] != None and i['HPHM'] != '-':
                        date = datetime.date(i['JGSJ'].year,i['JGSJ'].month,i['JGSJ'].day)
                        p_id = self.hphm_dict.get(i['HPHM'],-1)

                        if p_id !=-1 and self.mysql.getTraffic(date,p_id) == None:
                            traffic_set.add((date,p_id))

                self.mysql.addTraffic(list(traffic_set))
                self.id_ = hp_l[-1]['ID']
                self.fqIni.setSyst(self.id_)
                gl.TRIGGER.emit("<font %s>%s ID:%s %s</font>"%(gl.style_blue,self.hf.getTime(),self.id_,hp_l[-1]['JGSJ']))
                
            except MySQLdb.Error,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                logger.error(e)
                if e[0] == 1267:
                    pass
                if e[0] == 1062:
                    self.addMissPlate(miss_hphm)
                else:
                    self.loginmysqlflag = False
                    self.mysqlCount = 0
                    return
            except Exception,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                logger.error(e)
                if str(e)[:3] == 'ORA':
                    self.loginorcflag = False
                    self.orcCount==0
                    return
                else:
                    time.sleep(1)
                    pass

    #添加未缓存的车牌
    def addMissPlate(self,miss_hphm):
        for i in miss_hphm:
            try:
                p = self.mysql.getHphm(i)
                if p == None:
                    values = []
                    values.append(self.decomposeHphm(i.decode('gbk','ignore')))
                    newid = self.mysql.setHphm(values)
                    self.hphm_dict[i] = newid
            except MySQLdb.Error,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                logger.error('Error hphm:'+i)
                logger.error(e)
                if e[0] == 1062:
                    self.hphm_dict[i] = self.invalidhphm
                else:
                    self.loginmysqlflag = False
                    self.mysqlCount = 0
            except Exception,e:
                gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
                logger.error('Error hphm:'+i)
                logger.error(e)
                    
    #删除过期的fuzzy_id
    def delFuzzyHphm(self):
        t1 = datetime.datetime.now()-datetime.timedelta(hours=2)
        ot_fuzzyid = self.orc.getOTFuzzyHphm(t1.strftime('%Y-%m-%d %H:%M:%S'))
        if ot_fuzzyid !=[]:
            self.orc.delFuzzyHphmByID(ot_fuzzyid[0][0])
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_orange,self.hf.getTime()+' Fuzzyid: '+str(ot_fuzzyid[0][0])+' has been deleted'))
            logger.warning(' Fuzzyid: '+str(ot_fuzzyid[0][0])+' has been deleted')

    #加载车牌字典
    def setHphmDict(self):
        gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Loading hphm...'))
        try:
            #获取无效车牌'-'的ID
            p = self.mysql.getHphm('-')
            if p == None:
                values = [('-','__','__','__','__','__','__','__')]
                self.invalidhphm = self.mysql.setHphm(values)['l_id']
            else:
                self.invalidhphm = self.invalidhphm = p['id']
                
            i = 0
            while 1:
                offset = 10000
                l = self.mysql.getPlatecode(i,offset)
                i += offset
                if l == ():
                    break
                else:
                    for j in l:
                        self.hphm_dict[j['p1'].encode('gbk','ignore')] = j['id']
            self.hphmdictflag = True
        except MySQLdb.Error,e:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
            logger.error('Error hphm:'+i)
            logger.error(e)
            self.loginmysqlflag = False
            self.mysqlCount = 0
        except Exception,e:
            gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_red,self.hf.getTime()+str(e)))
            logger.error(e)
            time.sleep(1)

        gl.TRIGGER.emit("<font %s>%s</font>"%(gl.style_green,self.hf.getTime()+'Load done!'))

            
    #主循环
    def mainLoop(self):
        logger.info('Logon System')
        while 1:
            #退出检测
            if not gl.QTFLAG:
                gl.DCFLAG = False
                del self.orc
                del self.mysql
                del self.fqIni
                logger.warning('Logout System')
                break
                

            #登录检测
            if self.loginmysqlflag and self.loginorcflag and self.hphmdictflag:
                self.addTraffic()
            elif self.loginmysqlflag and self.hphmdictflag == False:
                self.setHphmDict()
            else:
                if not self.loginmysqlflag:
                    if self.mysqlCount==0 or self.mysqlCount > 15:
                        self.longinMysql()
                    else:
                        self.mysqlCount += 1

                if not self.loginorcflag:
                    if self.orcCount==0 or self.orcCount > 15:
                        self.loginOrc()
                    else:
                        self.orcCount += 1

                time.sleep(1)

if __name__ == "__main__":
    fq = FuzzyQ()
    fq.mainLoop()
    del fq








