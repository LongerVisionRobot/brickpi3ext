from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import sys
import math
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

class BrickPi3Ext(brickpi3.BrickPi3):
	
	def __init__(self):
		super(BrickPi3Ext, self).__init__()
		print(sys.version)
		print("Battery voltage: %6.3f\n9v voltage: %6.3f\n5v voltage: %6.3f\n3.3v voltage: %6.3f\n" % (self.get_voltage_battery(), self.get_voltage_9v(), self.get_voltage_5v(), self.get_voltage_3v3())) 
		self.set_motor_limits(self.PORT_A, 0, 0) 
		self.set_motor_limits(self.PORT_B, 0, 0) 
		self.set_motor_limits(self.PORT_C, 0, 0) 
		self.set_motor_limits(self.PORT_D, 0, 0)
		self.reset_motor_encoder(self.PORT_A) # reset encoder A
		self.reset_motor_encoder(self.PORT_B) # reset encoder B
		self.reset_motor_encoder(self.PORT_C) # reset encoder C
		self.reset_motor_encoder(self.PORT_D) # reset encoder D
	
	def motor_name_convert(self, port):
		if port == 1:
			return "A"
		elif port == 2:
			return "B"
		elif port == 4:
			return "C"
		elif port == 8:
			return "D"
		else:
			pass
	
	def reset_motor_encoder(self, port):
		self.offset_motor_encoder(port, self.get_motor_encoder(port))
		print("Motor %4s encoder is reset to zero" % (self.motor_name_convert(port)))
		
	def set_motor_On(self, port, power):
		try:
			self.set_motor_power(port, self.MOTOR_FLOAT)
			self.set_motor_power(port, power)
		except IOError as error:
			print(error)
	
	def set_motor_Off(self, port):
		try:
			self.set_motor_power(port, self.MOTOR_FLOAT)
		except IOError as error:
			print(error)
	
	def set_motor_OnForDegrees(self, port, motor_degrees, power = 0):
		try:		
			if power < 0:
				power = -1*power
				motor_degrees = -1*motor_degrees
			
			self.set_motor_limits(port, power, 0)
			self.reset_motor_encoder(port)
			self.set_motor_position(port, motor_degrees)
			print("Motor %4s movement initiated at %4i power" % (self.motor_name_convert(port), power))
			print("Target Degrees: %4i" % (motor_degrees))

			while True:
				difference = abs(motor_degrees-self.get_motor_encoder(port))
				print("Motor %4s Position: %6d  Difference to Target: %6d\r" % (self.motor_name_convert(port), self.get_motor_encoder(port),difference))
				time.sleep(0.25)
				if difference <= 6:
					print("Target reached with %3d degrees of error. \r" % (difference))
					break
		except IOError as error:
			print(error)
	
	def set_motor_MoveTankOnForDegrees(self, port1, port2, motor_degrees1, motor_degrees2, power1 = 0, power2 = 0):
		try:		
			if power1 < 0:
				power1 = -1*power1
				motor_degrees1 = -1*motor_degrees1
			
			if power2 < 0:
				power2 = -1*power2
				motor_degrees2 = -1*motor_degrees2
			self.set_motor_limits(port1, power1, 0)
			self.set_motor_limits(port2, power2, 0)
			self.reset_motor_encoder(port1)
			self.reset_motor_encoder(port2)
			self.set_motor_position(port1, motor_degrees1)
			self.set_motor_position(port2, motor_degrees2)
			
			print("Motor %4s movement initiated at %4i power" % (self.motor_name_convert(port1), power1))
			print("Target Degrees: %4i" % (motor_degrees1))
			print("Motor %4s movement initiated at %4i power" % (self.motor_name_convert(port2), power2))
			print("Target Degrees: %4i" % (motor_degrees2))

			while True:
				difference1 = abs(motor_degrees1-self.get_motor_encoder(port1))
				difference2 = abs(motor_degrees2-self.get_motor_encoder(port2))
				print("Motor %4s Position: %6d  Difference to Target: %6d  Motor %4s Position: %6d  Difference to Target: %6d\r" % (self.motor_name_convert(port1), self.get_motor_encoder(port1), difference1, self.motor_name_convert(port2), self.get_motor_encoder(port2), difference2))
				time.sleep(0.25)
				if difference1 <= 6 and difference2 <= 6:
					print("Motor %4s Target reached with %3d degrees of error. \r" % (self.motor_name_convert(port1), difference1))
					print("Motor %4s Target reached with %3d degrees of error. \r" % (self.motor_name_convert(port2), difference2))
					break
		except IOError as error:
			print(error)

