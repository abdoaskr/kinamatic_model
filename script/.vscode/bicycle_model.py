#!/usr/bin/env python3


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


def go_to_controller(x_goal, y_goal):
  global x 
  global y,z,yaw

  velocity_message =Twist()

  while(True):
    const_linear =0.5
    distance =abs( math.sqrt(((x_goal-x)**2) + (y_goal-y)**2)  )
    linear_speed = distance * const_linear

    const_angular = 4.0
    desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
    angular_speed = (desired_angle_goal - yaw)*const_angular

    velocity_message.linear.x =linear_speed
    velocity_message.angular.z =angular_speed

    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=10 )
  

    velocity_publisher.publish(velocity_message)
    print ("x=",x,'y=',y)

    if(distance < 0.01):
      break



if __name__ == '__main__':
  try:
    rospy.init_node('turtlesim_motion_pose', anonymous=True)
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=10 )
    pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, posecalback )
    time.sleep(2)
    
    x_goal=float(input("Set your x goal: "))
    y_goal=float(input("Set your y goal: "))
    go_to_controller( x_goal , y_goal)
  except rospy.ROSInterruptException:
    rospy.loginfo("node terminals")