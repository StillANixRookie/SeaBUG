#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64,String


class piston_position():
    def __init__(self):

        self.piston_pub = rospy.Publisher('Piston_Pose', Float64, queue_size=10)

        self.sub = rospy.Subscriber('Expansion', Float64, self.exp_update)
        self.expansion = 0
        rospy.init_node("piston_node")
        self.rate = rospy.Rate(2)

        self.piston_publisher()

    def piston_publisher(self):

        piston_pose = 0

        while not rospy.is_shutdown():

            piston_pose = self.expansion * 0.2

            self.piston_pub.publish(piston_pose)

            rospy.loginfo("Bladder expansion is %s and piston position is %s" % (self.expansion, piston_pose))

            self.rate.sleep()

    def exp_update(self, message):

        self.expansion = message.data

if __name__ == "__main__":
    try:
            piston_position()
    except rospy.ROSInterruptException:
        pass
