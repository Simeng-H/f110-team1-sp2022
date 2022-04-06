#!/usr/bin/env python
#F1/10 Team 1
from collections import deque
import math
import rospy
from race.msg import pid_input
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDrive
from std_msgs.msg import Float32MultiArray

class FTGController:
    car_radius = 0.3
    
    def __init__(self):
        rospy.init_node('ftg_controller', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        self.command_pub = rospy.Publisher('/car_1/offboard/command', AckermannDrive, queue_size = 10)
        rospy.Subscriber("/car_1/scan", LaserScan, self.scan_listener_hook)
    
    def scan_listener_hook(self, scan):
        pass

    def generate_control_message(self):
        pass

    def disparity_extend(self, scan):
        pass

if __name__ == '__main__':
    try:
        controller = FTGController()
    except:
        rospy.signal_shutdown()