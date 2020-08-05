#!/usr/bin/env python
# -*- coding: utf-8 -*- 


'''
导航 文件
'''
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid
import time
import math
import numpy as np
import numpy.linalg as LA
from move_base_msgs.msg import MoveBaseActionGoal

pub_map_x = rospy.Publisher("map_x", Float64, queue_size = 1)
map_x = Float64()
pub_map_y = rospy.Publisher("map_y", Float64, queue_size = 1)
map_y = Float64()

my_map = OccupancyGrid()
click_point = PointStamped()

map_pub = rospy.Publisher("map", OccupancyGrid, queue_size = 1)

def point_callback(data):      
    click_point.header = data.header
    click_point.point.x = data.point.x
    click_point.point.y = data.point.y 
    map_x.data = click_point.point.x
    map_y.data = click_point.point.y

    pub_map_x.publish(map_x)
    pub_map_y.publish(map_y)

    
if __name__ == '__main__':
    try:
        rospy.init_node('ZJ_play', anonymous = True)#初始化节点
	rospy.Subscriber("/clicked_point", 
                         PointStamped, 
                         point_callback)

   	
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
