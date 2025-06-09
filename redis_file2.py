#!/usr/bin/python3
import json
import os
import sys

current_path = os.path.abspath(__file__)
runpath = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
datapath=runpath+'/.file2redis/'
#import sys
#sys.path.append(runpath+"/../../dongfangcaifu")
#import dongfangcaifu as dc

class file4redis:
    
    def hget(self,filename,field):
        filename = datapath+filename+'.txt'
        try:
            with open(filename,'r',encoding='utf-8') as f:
                filedata=f.read()
        except:
            filedata='{}'
        filedata=json.loads(filedata)
        try:
            return filedata[field]
        except:
            return None
            
    def get(self,filename):
        filename = datapath+filename+'.txt'
        try:
            with open(filename,'r',encoding='utf-8') as f:
                filedata=f.read()
        except:
            filedata='{}'
        #filedata=json.loads(filedata)
        return json.loads(filedata)
        #return filedata

    def hset(self,filename_r,field,value_r):
        filename = datapath+filename_r+'.txt'
        try:
            with open(filename,'r',encoding='utf-8') as f:
                filedata=json.loads(f.read())
        except:
            if not os.path.exists(filename):
                filedata=json.loads('{}')
                print('merge kong file')
            else:             #不能接受对原有信息清空
                print('read file error...'+filename_r)
                exit()
        #filedata=json.loads(filedata)
        try:
            value=json.loads(value_r)
        except:
            value=value_r
            pass
        filedata[field]=value
        with open(filename,'w',encoding='utf-8') as f:
            f.write(json.dumps(filedata,ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
        os.system("echo `date +%H%M%S`',hset,"+filename_r+','+field+','+str(value_r).replace(' ','')+"'>>/root/tox/.file2redis/.actionlog/`date +%Y%m%d`.txt")
    
    def set(self,filename_r,value):
        filename = datapath+filename_r+'.txt'
        if type(value)==dict:
            filedata=value
        else:
            filedata=json.loads(value)
        with open(filename,'w',encoding='utf-8') as f:
            f.write(json.dumps(filedata,ensure_ascii=False, sort_keys=True, indent=4, separators=(', ', ': ')))
        os.system("echo `date +%H%M%S`',set,"+filename_r+','+str(value).replace(' ','')+"'>>/root/tox/.file2redis/.actionlog/`date +%Y%m%d`.txt")
     
    def merge(self,filename_r,content_r):
        filename = datapath+filename_r+'.txt'
        try:
            with open(filename,'r',encoding='utf-8') as f:
                filedata=json.loads(f.read())
        except:
            if not os.path.exists(filename):
                filedata=json.loads('{}')             #merge不能接受对原有信息清空
                print('merge kong file')
            else:
                #   print('read file error...')
                print('read file error...'+filename_r)
                exit()
        if type(content_r)!=dict:
            content=json.loads(content_r)
        else:
            content=content_r
        if filedata is not None:
            filedata.update(content)
        else:
            filedata=content
        with open(filename,'w',encoding='utf-8') as f:
            f.write(json.dumps(filedata,ensure_ascii=False, sort_keys=True, indent=4, separators=(', ', ': ')))
        os.system("echo `date +%H%M%S`',merge,"+filename_r+','+str(content_r).replace('<','\<').replace('>','\>').replace(' ','').replace("'","'\''")+"'>>/root/tox/.file2redis/.actionlog/`date +%Y%m%d`.txt")
    
    def mget(self,filenamelist):
        filedict=[]
        filenamelist=filenamelist.split(',')
        for filename in filenamelist:
            filename = datapath+filename+'.txt'
            try:
                with open(filename,'r',encoding='utf-8') as f:
                    filedata=f.read()
            except:
                filedata='{}'
            filedict+=[json.loads(filedata)]
        #filedata=json.loads(filedata)
        import pandas as pd

        # 设置显示的最大行数
        pd.set_option('display.max_rows', None)

        # 设置显示的最大列数
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)  #不换行

        res=pd.DataFrame(filedict)
        return res

            
if __name__ == '__main__':
    r=file4redis()
    #print(eval(r.hget('auth_dc_thl','cookies')))
    if len(sys.argv)==2:
        filename = datapath+sys.argv[1]+'.txt'
        with open(filename,'r',encoding='utf-8') as f:
            filedata=f.read()
            print(filedata)
        print(datapath+sys.argv[1]+'.txt')
    if sys.argv[1]=='get':
        print(r.get(sys.argv[2]))
    if sys.argv[1]=='hget':
        print(r.hget(sys.argv[2],sys.argv[3]))
    if sys.argv[1]=='set':
        r.set(sys.argv[2],sys.argv[3])
    if sys.argv[1]=='merge':
        r.merge(sys.argv[2],sys.argv[3])
    if sys.argv[1]=='hset':
        r.hset(sys.argv[2],sys.argv[3],sys.argv[4])

    if sys.argv[1]=='mget':
        if len(sys.argv)==4:
            ls=sys.argv[3].split(',')
            print(r.mget(sys.argv[2])[ls].to_string(line_width=sys.maxsize))
        else:
            #print(r.mget(sys.argv[2]).to_string(index=False, line_width=sys.maxsize))
            print(r.mget(sys.argv[2]).to_string(line_width=sys.maxsize))

    #mhset,给多个对象批量设置某个属性，涉及到写入操作，是否实现待分析
    #_filed,_file给属性及文本打更新时间信息
