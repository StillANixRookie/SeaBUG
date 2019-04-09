#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64


def depth_publisher():

    pub = rospy.Publisher('depth_publish', Float64, queue_size=10)

    rate = rospy.Rate(2)

    msg_to_publish = Float64()

    depth = 0
    a = 1

    while not rospy.is_shutdown():
        depth_to_publish = depth
        depth -= a*0.1

        if depth <-3:
            a = -1
        elif  depth > -0.2:
            a = 1


        msg_to_publish.data = depth_to_publish

        pub.publish(msg_to_publish)

        rospy.loginfo(depth_to_publish)

        rate.sleep()
if __name__ == "__main__":
    rospy.init_node("depth_publisher")
    depth_publisher()
