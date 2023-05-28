import rospy
from math import radians
import time
from nav_msgs.msg import Odometry
from tf import transformations
from std_msgs.msg import String
import numpy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def stop(vel_msg,vel_pub):
    vel_msg.linear.x = 0.0
    vel_msg.angular.z = 0.0
    print("stopping")
    vel_pub.publish(vel_msg)
    rospy.sleep(0.1)
    

def forward(vel_msg,vel_pub,forward_vel ):
    vel_msg = Twist()
    vel_msg.linear.x = forward_vel
    vel_msg.angular.z = 0.0
    vel_pub.publish(vel_msg)
    
    rospy.sleep(0.1)
    
        
    
def turnCCW(vel_msg,vel_pub,duration,front,angle):
    vel_msg = Twist()
    vel_msg.angular.z = radians(angle/duration)  
    rotate_duration = rospy.Duration.from_sec(duration) 
    start_time = rospy.Time.now()
    print("turning ccw")
    while rospy.Time.now() - start_time < rotate_duration:
        vel_pub.publish(vel_msg)
  
    stop(vel_msg,vel_pub)

    

def turnCW(vel_msg,vel_pub,duration,front,angle):
    vel_msg = Twist()
    vel_msg.angular.z = radians(- angle/duration)  
    rotate_duration = rospy.Duration.from_sec(duration)  
    start_time = rospy.Time.now()
    print("turning cw ")
    while rospy.Time.now() - start_time < rotate_duration:
    	
        vel_pub.publish(vel_msg)
	
    stop(vel_msg,vel_pub)
    
    

def spin(vel_msg,vel_pub,duration):    
    vel_msg = Twist()
    vel_msg.angular.z = radians(180/duration)  
    rotate_duration = rospy.Duration.from_sec(duration) 
    start_time = rospy.Time.now()
    print("rotating 180")
    while rospy.Time.now() - start_time < rotate_duration:
        vel_pub.publish(vel_msg)
        
    stop(vel_msg,vel_pub)
def solve_maze():
    vel_pub = rospy.Publisher(name='/cmd_vel', data_class=Twist, queue_size=10)
    
    while not rospy.is_shutdown():
        vel_msg = Twist()
        scan = rospy.wait_for_message('/scan', LaserScan)
        front = scan.ranges[0]
        right = scan.ranges[269]
        left = scan.ranges[89]
        front_right = scan.ranges[314]
        front_left = scan.ranges[44]
        var = min(front_left,front_right)

 
        if (front < 0.55) and (front < var):
            
            stop(vel_msg,vel_pub)
            print ("turn fully")
            if right < left :
                turnCCW(vel_msg,vel_pub,2,front,90)
            elif right > left:
                turnCW(vel_msg,vel_pub,2,front,90)
            elif (round(right,1) == round(left,1)) and (round(right,1) == 0.5) :
                spin(vel_msg,vel_pub,4)
            
        elif ( front < 0.55) and (front > var):
            
            stop(vel_msg,vel_pub)
            print("turn little")
            
            if right < left :
                turnCCW(vel_msg,vel_pub,1,front,22.5)
            elif right > left:
                turnCW(vel_msg,vel_pub,1,front,22.5)
            elif (round(right,1) == round(left,1)) and (round(right,1) == 0.5) :
                spin(vel_msg,vel_pub,4)
        else:
            forward(vel_msg,vel_pub,0.3)     

            
                

if __name__ == '__main__':
    rospy.init_node('maze_solver', anonymous=True)

    try:
        solve_maze()
    except rospy.ROSInterruptException:
        pass
