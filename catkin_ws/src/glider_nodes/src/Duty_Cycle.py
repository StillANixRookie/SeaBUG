#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64


def duty_publisher():

    pub = rospy.Publisher('Duty_Cycle', Float64, queue_size=10)

    rate = rospy.Rate(0.1)

    msg_to_publish = Float64()

    duty = 0
    a = 1

    while not rospy.is_shutdown():
        duty_to_publish = duty
        duty += a*10

        if duty >= 100:
            a = -1
        elif  duty <= 0:
            a = 1


        msg_to_publish.data = duty_to_publish

        pub.publish(msg_to_publish)

        rate.sleep()
if __name__ == "__main__":
    rospy.init_node("duty_publisher")
    duty_publisher()
