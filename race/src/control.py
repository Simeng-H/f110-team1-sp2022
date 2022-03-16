#!/usr/bin/env python
from collections import deque
import math
import rospy
from race.msg import pid_input
from ackermann_msgs.msg import AckermannDrive


class Controller:
	default_kp = 1.0
	default_kd = 1.0
	default_ki = 1.0
	default_vel = 15.0
	servo_offset = 0.0
	active_frequency = 100

	def __init__(self, active=False):
		"""
		@param active: whether to run in active mode, if in active mode, node publishes at fixed interval asynchronously with respect to receiving input, if in passive mode, node publishes each time input is received
		"""
		# error memory
		self.error_memory_size = 10
		self.error_memory = deque()

		# PID Control Params
		self.kp = Controller.default_kp
		self.kd = Controller.default_kd
		self.ki = Controller.default_ki
		self.vel = Controller.default_vel
		self.angle = 0.0

		# set mode
		self.active = active
		
		if self.active:
			# Active frequency
			self.frequency = Controller.active_frequency
			self.interval = 1/self.frequency

		# This code can input desired velocity from the user.
		# velocity must be between [0,100] to move forward. 
		# The following velocity values correspond to different speed profiles.
		# 15: Very Slow (Good for debug mode)
		# 25: Slow and steady
		# 35: Nice Autonomous Pace
		# > 40: Careful, what you do here. Only use this if your autonomous steering is very reliable.
		self.vel_input = Controller.default_vel

		# node config
		rospy.init_node('pid_controller', anonymous=False)
		rospy.on_shutdown(self.shutdown)


		rospy.Subscriber("error", pid_input, self.error_listener_hook)

		# Publisher for moving the car. 
		self.command_pub = rospy.Publisher('/car_1/offboard/command', AckermannDrive, queue_size = 10)

		if active:
			self.run_active()

	def generate_control_message(self):
		# An empty AckermannDrive message is created. You will populate the steering_angle and the speed fields.
		command = AckermannDrive()

		# print("PID Control Node is Listening to error")
		
		## Your PID code goes here
		
		# 1. Scale the error
		# 2. Apply the PID equation on error to compute steering

		p,i,d = self.get_pid()
		pid_output = self.kp * p + self.ki * i + self.kd * d
		# print("pid_output: ",pid_output)
		
		# convert pid_output_to steering angle through tanh function, *100 since range is [-100,100]
		self.angle = math.tanh(pid_output)*100

		command.steering_angle = self.angle
		command.speed = self.vel_input

		return command

	def register_pid_input(self, pid_input):
		# return
		error = pid_input.pid_error
		self.error_memory.append(error)
		if len(self.error_memory) >= self.error_memory_size:
			self.error_memory.popleft()

	def set_gains(self,kp, kd, ki, vel_input):
		self.kp = kp
		self.kd = kd
		self.ki = ki
		self.vel = vel_input
		
	def get_pid(self):
		if len(self.error_memory) == 0:
			return 0, 0, 0
		if len(self.error_memory) == 1:
			return self.error_memory[0], 0, 0
		p = self.error_memory[-1]
		i = sum(self.error_memory)
		d = self.error_memory[-1] - self.error_memory[-2]
		return p,i,d

	def run_active(self):
		while not rospy.is_shutdown():
			control_msg = self.generate_control_message()
			self.command_pub.publish(control_msg)
			rospy.sleep(self.interval)

	def error_listener_hook(self, pid_input):
		self.register_pid_input(pid_input)

		# If in passive mode: need listener to trigger publication
		if not self.active:
			control_msg = self.generate_control_message()
			self.command_pub.publish(control_msg)

	def shutdown(self):
		rospy.sleep(0.1)
		print("Shutting down")


if __name__ == '__main__':
	# kp = int(input("Enter Kp Value: "))	
	# kd = int(input("Enter Kd Value: "))
	# ki = int(input("Enter Ki Value: "))
	# vel_input = int(input("Enter desired velocity: "))
	try:
		controller = Controller(active=False)
	except:
		rospy.signal_shutdown()
	
	rospy.spin()
	# controller.set_gains(kp, kd, ki, vel_input)
