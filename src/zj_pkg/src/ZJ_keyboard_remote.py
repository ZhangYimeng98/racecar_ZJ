#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#ZJ2020

'''
这是键盘遥控文件
用四个方向键控制
'''
import rospy
import pygame as pg  # pygame 包来读取键盘
from std_msgs.msg import Float64
import time

pub_speed = rospy.Publisher("zj_control_cmd/speed", Float64, queue_size = 1)#速度publisher
pub_turn  = rospy.Publisher("zj_control_cmd/turn",  Float64, queue_size = 1)#转向publisher
speed_data=Float64()
turn_data=Float64()


#参数，线速度参数和角速度参数
SET_LINE_SPEED = 10  #设置线速度
SET_ROTATE_SPEED = 30 #设置转角

if __name__ == '__main__':
        
    #初始化节点
    rospy.init_node('ZJ_keyboard_remote', anonymous = True)

    # pygame初始化
    pg.init()
    window = pg.display.set_mode((320, 240))
    pg.display.set_caption("ZJ_control_window(pygame)")

    # 正常运行
    end_flag = False

    last_v_line=0.0
    last_v_rotate=0.0
    while not end_flag:
        #pg.time.delay(30)
        time.sleep(0.03)

        # 显示，背景色
        window.fill((100, 100, 100))

        # pygame处理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end_flag = True # 当窗口被关闭时，end_flag为真，退出循环
        v_line = 0.0
        v_rotate = 0.0

        # 检测按键，并遥控小车，并更新显示
        key_status = pg.key.get_pressed()
        window_block_position = [160 - 25, 120 - 25]

        if key_status[pg.K_UP] == 1:
            window_block_position[1] -= 100
            v_line += SET_LINE_SPEED
        if key_status[pg.K_DOWN] == 1:
            window_block_position[1] += 100
            v_line -= SET_LINE_SPEED
        if key_status[pg.K_LEFT] == 1:
            window_block_position[0] -= 100
            v_rotate -= SET_ROTATE_SPEED
        if key_status[pg.K_RIGHT] == 1:
            window_block_position[0] += 100
            v_rotate += SET_ROTATE_SPEED

        # 显示矩形
        pg.draw.rect(window, (255, 0, 0), (window_block_position[0], window_block_position[1], 50, 50))
        # 发送速度
        if last_v_line!=v_line:
            speed_data.data=v_line
            last_v_line=v_line
            pub_speed.publish(speed_data)
        
        if last_v_rotate!=v_rotate:
            turn_data.data=-v_rotate  #负值右转，所以加个负号
            last_v_rotate=v_rotate
            pub_turn.publish(turn_data)

        #更新pygame显示
        pg.display.update()

    #退出（控制窗口关闭）
    pg.quit()
    print("ZJ_KEYBOARD_REMOTE exit")
