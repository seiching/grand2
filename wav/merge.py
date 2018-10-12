#改用讀參數
#encoding=utf-8
#merg 資料庫
#encoding=utf-8
#merg 資料庫
import sqlite3
import os
import sys
if len(sys.argv) < 3: # 1
        print( "Usage:", sys.argv[0], " A ADB")
        sys.exit(1)       # 2
part = sys.argv[1]
directory=sys.argv[2]
#directory= input(">>> Input which part directory , please check the folder : ")
#part= input(">>> Input which part only accept A,B,C, please check the folder : ")
part=part.upper()
directory=directory.upper()
print('part=',part,'  directory=',directory)
conn = sqlite3.connect('grand.db')
try:
  sql="delete from  %spart "  %(part)
  print(sql)
  conn.execute(sql )
  conn.commit()
  print('delete success')
except Exception as e:
  print("Failed delete "+ str(e))
  sys.exit()
#  pass


  
objects = os.listdir(directory)  # find all objects in a dir
result=[]
j=0
#conn desitionation db connection
#source db filename
#part number
def mergedb(conn,filename,part):
    src = sqlite3.connect(filename)
    cursor = src.cursor()
    sql="SELECT filename, sentence from  part ;"  
  # pdgrand=pd.read_sql(sql,src)
   # print(filename,'=',len(pdgrand))
    for i in cursor.execute(sql):
    
      filename=i[0]
      sentence=i[1]
      sentence=sentence.replace('，','')
      sentence=sentence.replace('。','')
      sentence=sentence.replace(',','')
      sentence=sentence.replace('XXXX','')  
      if 'XXXX,'==sentence:
            print('skip',filename,sentence)
            continue
      ID=int(filename[4:8])
      try:
        sql="insert into %spart (filename, sentence,ID) VALUES('%s', '%s',%d)"  %(part,filename.upper(), sentence,ID)
        conn.execute(sql )
      except Exception as e:
        print("Failed insert db: "+ str(e)) 
        print(sql)
    conn.commit()
    
    src.close()
j=0    
for i in objects:  # check if very object in the folder ...
    
    dbfilename= os.path.join(directory, i)
    if os.path.isfile(dbfilename) and dbfilename[-2:]=='db':
      print(dbfilename)
      mergedb(conn,dbfilename,part)

conn.commit()
conn.close() 


