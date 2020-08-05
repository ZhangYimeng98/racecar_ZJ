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
import time
import math
import numpy as np
import numpy.linalg as LA
from move_base_msgs.msg import MoveBaseActionGoal

#from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
'''-------------global param----------------'''
point_width = 40
mid_point = 80
'''-------------global param----------------'''

pub_speed = rospy.Publisher("zj_control_cmd/speed", Float64, queue_size = 1)
pub_turn = rospy.Publisher("zj_control_cmd/turn", Float64, queue_size = 1)
pub_curvature = rospy.Publisher("zj_control_cmd/curvature", Float64, queue_size = 1)


pub_point1 = rospy.Publisher("point1", PointStamped, queue_size = 1)
pub_point2 = rospy.Publisher("point2", PointStamped, queue_size = 1)
pub_point3 = rospy.Publisher("point3", PointStamped, queue_size = 1)

point1 = PointStamped()
point2 = PointStamped()
point3 = PointStamped()

speed_data=Float64()
turn_data=Float64()
min_curvature = Float64(1000.0)
'''-----------------stop car------------------'''
goal_point_x = Float64()
goal_point_y = Float64()
odom_point_x = Float64()
odom_point_y = Float64()
odom_yaw = Float64()
def odom_callback(data):
    global odom_point_x
    global odom_point_y
    global odom_yaw
    odom_point_x = data.pose.pose.position.x
    odom_point_y = data.pose.pose.position.y
    odom_yaw = data.twist.twist.angular.z
def get_goal_callback(data):
    global goal_point_x
    global goal_point_y
    goal_point_x = data.goal.target_pose.pose.position.x
    goal_point_y = data.goal.target_pose.pose.position.y
'''-----------------sopt car------------------'''

def lenth_cal(x1,x2,y1,y2):
    x = (x1 - x2)**2
    y = (y1 - y2)**2
    l = np.sqrt(x+y)
    return l

def radius_cal(a,b,c):
    p = (a+b+c)/2.0
    s = np.sqrt(p*(p-a)*(p-b)*(p-c))
    r = (a*b*c)/4.0/s
    return r



def cmd_vel_callback(data):
    global min_curvature
    stop_flag = Float64(lenth_cal(float(odom_point_x) , float(goal_point_x) , float(odom_point_y) , float(goal_point_y)))
    if stop_flag.data <= 1.5:
        speed_data.data = 0
        turn_data.data = 0
    else:
        turn_data.data=data.angular.z*0.7
        if min_curvature.data <= 3:
            speed_data.data= 15+5*(min_curvature.data/3) #data.linear.x*180  #20
        else:
            speed_data.data= 30 #32 #data.linear.x*240   #38
        #if(math.fabs(turn_data.data)<10):
        #    turn_data.data*=1.0
        #    speed_data.data=data.linear.x*220    #20-math.fabs(turn_data.data)*1.0
        #    
        #else:
        #    speed_data.data=data.linear.x*220      #5
        
    pub_curvature.publish(min_curvature)
    pub_speed.publish(speed_data)
    pub_turn.publish(turn_data)




def path_callback(data):       
    if len(data.poses) <= point_width*2:
        index1 = 0
        index2 = (len(data.poses)-1)//2
        index3 = len(data.poses)-1
    elif (len(data.poses) > (point_width*2)) and (len(data.poses) <= (mid_point+point_width)):
        index1 = (len(data.poses)-1)-(point_width*2)
        index2 = (len(data.poses)-1)-point_width
        index3 = len(data.poses)-1
    elif len(data.poses) > (mid_point+point_width):
        index1 = mid_point-point_width
        index2 = mid_point
        index3 = mid_point+point_width
    else:
        index1 = index2 = index3 = 0


    point1.header.frame_id = 'map'
    point1.point.x = data.poses[index1].pose.position.x
    point1.point.y = data.poses[index1].pose.position.y
    pub_point1.publish(point1)

    point2.header.frame_id = 'map'
    point2.point.x = data.poses[index2].pose.position.x
    point2.point.y = data.poses[index2].pose.position.y
    pub_point2.publish(point2)

    point3.header.frame_id = 'map'
    point3.point.x = data.poses[index3].pose.position.x
    point3.point.y = data.poses[index3].pose.position.y
    pub_point3.publish(point3)

    if index1 >= 0:
        global min_curvature
        min_curvature = Float64(1000.0)
        for i in range(0,index1): 
            len1 = lenth_cal(data.poses[index1-i].pose.position.x , data.poses[index2-i].pose.position.x , data.poses[index1-i].pose.position.y , data.poses[index2-i].pose.position.y)
            len2 = lenth_cal(data.poses[index2-i].pose.position.x , data.poses[index3-i].pose.position.x , data.poses[index2-i].pose.position.y , data.poses[index3-i].pose.position.y)
            len3 = lenth_cal(data.poses[index1-i].pose.position.x , data.poses[index3-i].pose.position.x , data.poses[index1-i].pose.position.y , data.poses[index3-i].pose.position.y)
            curvature = Float64(radius_cal(len1 , len2 , len3))
            if curvature.data <= min_curvature.data:
                min_curvature.data = curvature.data
    #k1 = Float64((data.poses[index1].pose.position.y - data.poses[0].pose.position.y)/(data.poses[index1].pose.position.x - data.poses[0].pose.position.x))
    #k2 = Float64((data.poses[index2].pose.position.y - data.poses[index1].pose.position.y)/(data.poses[index2].pose.position.x - data.poses[index1].pose.position.x))
    #k_err = Float64(k2.data - k1.data)
   
    
if __name__ == '__main__':
    try:
        rospy.init_node('ZJ_play', anonymous = True)#初始化节点
        rospy.Subscriber("cmd_vel", 
                         Twist, 
                         cmd_vel_callback)
        rospy.Subscriber("/move_base/TebLocalPlannerROS/global_plan", 
                         Path, 
                         path_callback)       
        rospy.Subscriber("/move_base/goal", 
                         MoveBaseActionGoal, 
                         get_goal_callback)
        rospy.Subscriber("/odom_rf2o", 
                         Odometry, 
                         odom_callback) 
        

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
