# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 16:31:44 2018

@author: lenovo
"""

import pycurl
import wave
from pyaudio import PyAudio,paInt16
import urllib.request
import json

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*10:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file('01.wav',my_buf)
    stream.close()

def get_token():
    apiKey="tqABH7ABfrnloqAW5gqgN084" #
    secreKey="y1jSboC1ogsVGjKqeeoGiWUwVmZKLQ6v" 
    auth_url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+apiKey+"&client_secret="+secreKey;

    res=urllib.request.urlopen(auth_url)
    json_data=res.read()
    print('type:',type(json_data))
    return json.loads(json_data)['access_token']

def dump_res(buf):
    #print('buf=',buf)
    #tem=speaktext()
    
    my_temp=json.loads(buf)
    if(my_temp['err_no']==3301):
        print('识别失败')
        return
    my_list=my_temp['result']
    #print(type(my_list))
    #print('mylist[0]: ',my_list[0])
    #return ''.join(my_list)
    
    
def use_cloud(token):
    fp=wave.open('01.wav','rb')
    nf = fp.getnframes()  # 获取文件的采样点数量
    #print('sampwidth:', fp.getsampwidth())
    #print('framerate:', fp.getframerate())
    #print('channels:', fp.getnchannels())
    f_len = nf * 2  # 文件长度计算，每个采样2个字节
    audio_data = fp.readframes(nf)

    cuid="XXXXXXXXXXX"
    srv_url='http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' +token
    http_header=[
        'Content-Type:audio/pcm;rate=8000',
        'Content-Length: %d' % f_len
    ]
    c=pycurl.Curl()
    c.setopt(pycurl.URL,str(srv_url)) #curl doesn't support unicode 传递一个网址
    #c.setopt(c.RETURNTRANSFER,1)
    c.setopt(c.HTTPHEADER,http_header)#传入一个头部，只能是列表，不能是字典
    c.setopt(c.POST,1)#发送
    c.setopt(c.CONNECTTIMEOUT,80)#尝试连接时间
    c.setopt(c.TIMEOUT,80)#下载时间
    c.setopt(c.WRITEFUNCTION,dump_res)
    c.setopt(c.POSTFIELDS,audio_data)
    c.setopt(c.POSTFIELDSIZE,f_len)
    c.perform() # pycurl.perform() has no return val
    

    
    
#test
if __name__ == '__main__':
    my_record()
    print('over!!!!')
    use_cloud(get_token())
    #print(tem.text)
