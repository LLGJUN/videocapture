# coding:utf-8
import cv2
from datetime import datetime
import numpy as np
cap = cv2.VideoCapture(1)  # 创建一个 VideoCapture 对象
cap.set(3, 640)
cap.set(4, 480)

flag = 1  # 设置一个标志，用来输出视频信息
while (cap.isOpened()):  # 循环读取每一帧

    ret_flag, frame = cap.read(1)
    # gray = cv2.cvtColor(Vshow,cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray",gray)
    print(ret_flag)
    time_str = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, time_str, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.imshow("Capture_Test", frame)  # 窗口显示，显示名为 Capture_Test

    k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
    if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
        print(cap.get(3))
        print(cap.get(4))

    elif k == ord('q'):  # 若检测到按键 ‘q’，退出
        break

cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 删除建立的全部窗口