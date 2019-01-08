*******************************************************
多路摄像头视频采集程序
by linjunji QQ:1360622136 date 2019-01-08
*******************************************************

运行方法
1、直接点击capturevideo_yunnanproject.exe文件就可以进行视频采集，保存的视频文件放在和.exe文件同级的目录下
文件命名方式为（camera_name_localtime.avi）

配置文件config.ini详解
[camera_para]
height=分辨率
width=分辨率
fps=帧率
each_file_time=单个视频保存时间，单位秒
load_loc_time=True or False 是否在图片上加载时间

[camera_name]
CAM1=rmoncam CAM1    rmoncam CAM1为摄像机名称，可以通过设备管理器查看并修改，目前最多支持6个摄像机
CAM2=rmoncam CAM2
CAM3=rmoncam CAM3
CAM4=rmoncam CAM4
CAM5=rmoncam CAM5
CAM6=rmoncam CAM6

[video_folder]
CAM1=cam1_video    cam1_video 为要保存的视频文件夹名称，每个摄像头对应一个文件夹
CAM2=cam2_video
CAM3=cam3_video
CAM4=cam4_video
CAM5=cam5_video
CAM6=cam6_video