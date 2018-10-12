#encoding=utf-8
import sqlite3
import pandas as pd
def findq4posold(sentence,q4,percent):
    try:
        pos4trystart=int(len(sentence)*percent)
        q4try=sentence[pos4trystart:]
        po4start=q4try.find(q4) 
        if (po4start<0):
            return -1,q4try
        q4=sentence[pos4trystart+q4try.find(st)+1:]
        return po4start, pos4trystart,q4
    except Exception as e:
        print('find4posold error'+str(e))
def findq4pos(sentence,q4,percent):
    try:
        if q4=='':
            return -1,pos4trystart,q4try   
        pos4trystart=int(len(sentence)*percent)
        q4try=sentence[pos4trystart:]
        po4start=q4try.find(q4) 
        #print('q4try',q4try,'start=',po4start)
        if (po4start<0):
            return -1,pos4trystart,q4try
        q4=sentence[pos4trystart+po4start+1:]
        return po4start, pos4trystart,q4
    except Exception as e:
        print('find4pos error'+str(e))
def findq4(sentence,q4possible,percent):
    try:   
        for st in q4possible:
            po4start, pos4trystart,q4= findq4pos(sentence,st,percent)
            if (po4start!=-1):
                break
        if( po4start==-1):
            # print('not found')
            #nfound=nfound+1
          position4=int(len(sentence)*0.75)
        else:
            position4= po4start+pos4trystart
        return position4,q4,po4start
    except Exception as e:
        print("find q4 error : "+ str(e)) 
        return 0,q4,po4start       
def findq2pos(sentence,q2,pos2start,percent):
    try:
        pos2tryend=int(len(sentence)*percent)
        q2try=sentence[pos2start:pos2tryend]
        #print('q2try',q2try)
        po2start=q2try.find(q2) 
        #print('po2start',po2start)
        #if(po2start==-1):
        #print('not found q2try',q2try) 
        return po2start
    except Exception as e:
        print('findq2pos error'+str(e))
def findq3pos(sentence,q3,pos3start,pos4start):
   #pos2tryend=int(len(sentence)*percent)
  # q3='三'
    try:
        pos3end=pos4start-1
        q3try=sentence[pos3start:pos3end]
        #print('q3=',q3,'q3try',q3try)
        po3start=q3try.find(q3) 
        #print('po2start',pos3start)
        #if(po3start==-1):
        #print('q3try',q3try) 
        return po3start
    except Exception as e:
        print('findq3pos error'+str(e))
def spiltc(conn):
    try:
    #conn = sqlite3.connect('grand.db')
        sql="SELECT filename, sentence,position4 FROM Cpart;"
        pdgrand=pd.read_sql(sql,conn)
        q4=""
        qrtry=""
        q4possible=['是','4','市','式','四','是','世','室','事','試','士','似','適','示','伺','寺','釋']  
        q2possible=['2','二']
        q3possible=['山','3','三','參']
        q1possible=['1','一','壹'] 
        #for i in range(len(pdgrand)):
        nfound=0
        for i in range(len(pdgrand)):
            #for i in range(100):
            cuterror=0
            filename=pdgrand.filename.values[i]
            q4notfound=0
            sentence=pdgrand.sentence.values[i]
            # print(filename,sentence)
            if sentence is None :
                print(filename,sentence)
                continue
                #sentence='1.5公里21點4公里山1.3公里是1.6公里 '
                #position4=pdgrand.position4.values[i]
            position4,q4,q4notfound=findq4(sentence,q4possible,0.6)
            #print('after findq4')
            if(q4notfound==-1):
                #print(filename)
                nfound=nfound+1
                cuterror=1
            q2startinit=2
            for st in q2possible:
                position2= findq2pos(sentence,st,q2startinit,0.5)
                if (position2!=-1):
                    break
            if(position2==-1):
                #print('not found')
                nfound=nfound+1
                cuterror=1
                position2=int(len(sentence)*0.25)
            else:
                position2=position2+q2startinit
                #print('q2=',q2position)
                # q1=sentence[1:position2]
            #print('after findq2')
            if sentence[0:1] in  q1possible:
                q1=sentence[1:position2] #辨識時加了offset 跳過一秒
            else:
                q1=sentence[0:position2] #辨識時加了offset 跳過一秒
            for st in q3possible:
                position3=findq3pos(sentence,st, position2,position4)
                #print('loopq3',position3,st,'len sentence=',len(sentence))
                if (position3!=-1):
                    break
            if(position3==-1):
                #print('q3 not found')
                nfound=nfound+1
                cuterror=1
                position3=int(len(sentence)*0.5)
            else:
                position3=position3+position2+1
            q3=sentence[position3:position4]
           # print('after q3')
            #print('position3=',position3)
            q2=sentence[position2+1:position3-1]
            sql="update Cpart set Q1='%s',Q2='%s',Q3='%s',Q4='%s',position2=%d,position3=%d,position4=%d,cuterror=%d\
                where filename='%s' "  %(q1,q2,q3,q4,position2,position3,position4,cuterror,filename) 
            conn.execute(sql )
            #print('after exec')
            #print('sentence=',sentence,' q1=',q1,' q2=',q2,' q3=',q3,'q4=',q4)
        print('nfound=',nfound,'total=',len(pdgrand))
        conn.commit()
    except Exception as e:
        print('spilt c error'+str(e))



