# -*- coding: utf-8 -*-
# !/usr/bin/env python
#  同时进行多个摄像头录制，并将摄像头视频进行保存下来,
#1 能够开机重启
#2 能够将多个摄像头数据分文件夹进行保存
#3 视频保存的时间长短
#4 能够检测哪个摄像头没有开启，能够重启摄像头进行重摄像
#5 能够查看摄像头的显示界面
#6 有配置文件，能够根据配置文件进行数据格式化处理
#摄像头如何编号，摄像头插拔怎么处理

import cv2
import threading
import os
import datetime
import time
import configparser

#读取配置文件
cf=configparser.ConfigParser()
try:
    cf.read('config.ini')
    #拍摄分辨率
    video_width=int(cf.get('camera_para','width'))
    video_height=int(cf.get('camera_para','height'))
    fps=int(cf.get('camera_para','fps'))            #视频拍摄的帧率 帧/s
    each_file_time=int(cf.get('camera_para','each_file_time')) #每个文件保存的时间，单位秒
    is_load_time=bool(cf.get('camera_para','load_loc_time')) #是否图片加载时间

    #定义摄像头名称
    CAM1=cf.get('camera_name','CAM1')   #前视视频
    CAM2=cf.get('camera_name','CAM2')   #后视视频
    CAM3=cf.get('camera_name','CAM3')
    CAM4=cf.get('camera_name','CAM4')
    CAM5=cf.get('camera_name','CAM5')
    CAM6=cf.get('camera_name','CAM6')

    #定义摄像头和存储的文件夹的对应关系
    ID_FOLDER={CAM1:cf.get('video_folder','CAM1'),
               CAM2:cf.get('video_folder','CAM2'),
               CAM3:cf.get('video_folder','CAM3'),
               CAM4:cf.get('video_folder','CAM4'),
               CAM5:cf.get('video_folder','CAM5'),
               CAM6:cf.get('video_folder','CAM6')}
except:
    print('配置文件读取异常，请检查！')

#定义读取摄像头状态信息exe文件名
EXE_FILE_NAME='getcameraid.exe'

#获取视频图像句柄
class  deal_video_stream():
    def __init__(self,num,width,height,fps):
        self.num=num
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video_width=width
        self.video_height=height
        self.fps=fps

    #返回值 null 表示设备读取异常
    def get_video_capture_status(self):
        self.capture=cv2.VideoCapture(self.num)
        if self.capture.isOpened():
            return True
        else:
            return False

    def set_video_writer(self,filename):
        self.outfile=cv2.VideoWriter(filename,self.fourcc,self.fps,(self.video_height,self.video_width))

    def read_frame_from_video(self):
        ret,frame=self.capture.read()
        return ret,frame

    def write_frame_to_video(self,frame):
        self.outfile.write(frame)

    def destory_cap(self):
        self.capture.release()

#初始传入参数是相机名称，相机ID，当摄像头检测失败之后，就根据名称重新计算ID
def start_log_video_(cam_num,cam_name,width,height,fps):
    is_close=False  #设备是否关闭标志
    num=cam_num   #摄像机的索引
    name=cam_name  #摄像机的名称
    while True:
        if  is_close:  #重新计算ID
            camera_num, camera_name_id = get_cameras_status(EXE_FILE_NAME)
            print(camera_name_id)
            try:
                num=camera_name_id[name]
            except:
                continue
        video_cap=deal_video_stream(num,width,height,fps)
        if video_cap.get_video_capture_status():
            is_close=False
            #print('设备'+str(name)+'正常')
        else:
            is_close=True
            continue
            #print('设备'+str(name)+'异常')

        #创建文件存储路径
        current_path=os.getcwd()
        if not os.path.exists(ID_FOLDER[name]):
            os.mkdir(ID_FOLDER[name])
        new_path=ID_FOLDER[name]
        pathname=os.path.join(current_path,new_path)
        while( not is_close):
            T1 = datetime.datetime.now()
            filename = os.path.join(pathname,str(name) + '_' + T1.strftime("%Y-%m-%d %H-%M-%S") + '.avi')
            video_cap.set_video_writer(filename)
            T1 = datetime.datetime.now()
            while(True):
                ret,frame=video_cap.read_frame_from_video() #存在视频数据时，ret返回true 否则返回False
                if ret:
                    if is_load_time:
                        time_str = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                        cv2.putText(frame, time_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                    video_cap.write_frame_to_video(frame)
                else:
                    print('摄像头'+str(name)+'已经关闭')
                    is_close=True
                    break
                T2=datetime.datetime.now()
                if (T2-T1).seconds>each_file_time:  #十秒钟保存为一个文件
                    break

# 初始传入参数是相机名称，相机ID，当摄像头检测失败之后，就根据名称重新计算ID
def start_log_video(num,name, width, height, fps):
    print('线程'+str(name)+'启动成功')
    global  thread_stop_flag
    video_cap = deal_video_stream(num, width, height, fps)
    if video_cap.get_video_capture_status():
        # print('设备'+str(name)+'正常')
        pass
    else:
        print('线程' + str(name) + '结束')
        return 0
        # print('设备'+str(name)+'异常')
    # 创建文件存储路径
    current_path = os.getcwd()
    if not os.path.exists(ID_FOLDER[name]):
        os.mkdir(ID_FOLDER[name])
    new_path = ID_FOLDER[name]
    pathname = os.path.join(current_path, new_path)

    while (not thread_stop_flag):
        T1 = datetime.datetime.now()
        filename = os.path.join(pathname,str(name) + '_' + T1.strftime("%Y-%m-%d %H-%M-%S") + '.avi')
        video_cap.set_video_writer(filename)
        T1 = datetime.datetime.now()
        while (not thread_stop_flag):
            ret, frame = video_cap.read_frame_from_video()  # 存在视频数据时，ret返回true 否则返回False
            if ret:
                if is_load_time:
                    time_str = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frame, time_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),1)
                video_cap.write_frame_to_video(frame)
            T2 = datetime.datetime.now()
            if (T2 - T1).seconds > each_file_time:  # 十秒钟保存为一个文件
                break
    print('线程' + str(name) + '结束')

#获取摄像头对应的ID和名称信息，返回值为字典
def get_cameras_status(filename):
        camera_name_id={}
        camera_num=0
        if os.path.exists(filename):
            text=os.popen(filename).read()  #读取运行结果
            lines=text.split('\n')         #第一行为相机个数，剩下行为ID和名称
            camera_num=int(lines[0].split(':')[1])   #得到相机个数
            if camera_num==0: #当前没有摄像机
                print('当前程序没有检测到摄像机的存在，请检查连接情况！')
            else:
                for i in range(1,camera_num+1):
                    NAME=lines[i].split(':')[3]
                    ID=int(lines[i].split(':')[1])
                    camera_name_id[NAME]=ID
        else:
            print(filename+'文件不存在，请联系开发人员！')
        return text,camera_num,camera_name_id

#检测摄像机的状态，若有新摄像机插拔，则重启程序
def check_new_device():
    global  thread_stop_flag
    text,camera_num, camera_name_id = get_cameras_status(EXE_FILE_NAME)
    device_set=camera_name_id.keys()
    while(True):
        text,camera_num, camera_name_id = get_cameras_status(EXE_FILE_NAME)
        new_device_set=camera_name_id.keys()
        if new_device_set!=device_set:
            thread_stop_flag=True
            device_set=new_device_set
            print('检测到摄像头有插拔情况，重启录像线程'+'\n')
            #等待线程重启
            while(thread_stop_flag):
                pass
        time.sleep(1)


#全局变量，定义是否重启录像线程
global thread_stop_flag
thread_stop_flag=False

if __name__ == '__main__':
    #开始摄像头状态检测线程
    t = threading.Thread(target=check_new_device, args=())
    t.setDaemon(True)
    t.start()

    while(True):
        text,camera_num,camera_name_id=get_cameras_status(EXE_FILE_NAME)
        print('当前摄像机信息如下：')
        print(text)
        print('正在启动录像线程......')
        thread_set = []
        for key in camera_name_id.keys():
            t = threading.Thread(target=start_log_video, args=(camera_name_id[key],key,video_width,video_height,fps))  # 创建线程
            t.setDaemon(True)  #设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
            t.start() #开启线程
            thread_set.append(t)

        # 等待所有录像线程结束
        while(1):
            isalive=False
            for t in thread_set:
                flag=t.is_alive()
                isalive=isalive | flag
            if not isalive:
                break

        # print('debug123')
        thread_stop_flag=False
