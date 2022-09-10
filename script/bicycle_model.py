#!/usr/bin/env python3


from cmath import atan, cosh
from sqlite3 import Time
from turtle import distance
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x=0
y=0
z=0
yaw=0

def posecalback(pose_message):
  global x
  global y ,z , yaw
  x=pose_message.x
  y=pose_message.y
  yaw =pose_message.theta


def go_to_controller(velocity,slooping_angle_in_D,time_of_simulation):
  global x 
  global y,z
  
  velocity_message =Twist()
  t0=rospy.Time.now().to_sec()
  rate = rospy.Rate(10)
  while not rospy.is_shutdown(): 
    
    velocity_message.linear.x =velocity
    velocity_message.angular.z =slooping_angle_in_D*time_of_simulation
    
    
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=10 )
    t1=rospy.Time.now().to_sec()
    
    time_of_simulation=(t1-t0)
    rate.sleep()
    
    velocity_publisher.publish(velocity_message)
    
    print ("x=",x,'y=',y)
    


if __name__ == '__main__':
  try:
    rospy.init_node('turtlesim_motion_pose', anonymous=True)
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=10 )
    pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, posecalback )
    time.sleep(2)

    
    distance_form_front_wheel=4
    distance_from_back_wheel=3
    
    velocity=float(input("Input velocity: "))
    steering_angle=float(input("Input steering angle: "))
    time_of_simulation=float(input("Input Time of simulation: "))
   
    steering_angle_in_D=(steering_angle*180)/3.14
    
    velocity=velocity*time_of_simulation

    sliping_angle_in_D=abs(math.degrees(math.atan(distance_from_back_wheel/(distance_from_back_wheel+distance_form_front_wheel))*math.tan(steering_angle_in_D)))
   
    slope_angle_in_D=abs(velocity/(distance_form_front_wheel+distance_from_back_wheel)*(math.cos(sliping_angle_in_D)*math.tan(steering_angle_in_D)))
  
    go_to_controller( velocity,slope_angle_in_D,time_of_simulation)
  except rospy.ROSInterruptException:
    rospy.loginfo("node terminals")





