#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Float64


class actuator_demand():
    def __init__(self):

        self.sub1 = rospy.Subscriber('Duty_Cycle', Float64, self.duty_cycle_update)
        rospy.init_node("actuator_node")
        self.rate = rospy.Rate(0.1)

    def GPIO_PIN(self):

        pin_front_s = 11
        f = 1000

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(front_S, GPIO.OUT)

        GPIO.output(front_S, True)

        front_s = GPIO.PWM(pin_front_s, f)
        front_s.start(0)

        while not rospy.is_shutdown():

            front_s_dc = self.dutycycle_front_s
            front_s.ChangeDutyCycle(front_s_dc)

            self.rate.sleep()

    def duty_cycle_update(self, message):

        self.dutycycle_front_s = message.data

if __name__ == "__main__":
    try:
        actuator_demand()
    except rospy.ROSInterruptException:
        pass
