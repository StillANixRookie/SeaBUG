#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64,String


class bladder_exp():
    def __init__(self):

        self.expansion_pub = rospy.Publisher('Expansion', Float64, queue_size=10)

        self.sub = rospy.Subscriber('state', String, self.state_update)
        self.state = "descend"
        rospy.init_node("expansion_node")
        self.rate = rospy.Rate(2)

        self.expansion_publisher()

    def expansion_publisher(self):

        expansion = 1

        while not rospy.is_shutdown():

            if self.state == 'descend':
                expansion = -1
            elif self.state == 'ascend':
                expansion = 1

            self.expansion_pub.publish(expansion)

            rospy.loginfo("Glider state is %s m and bladder expansion is %s" % (self.state, expansion))

            self.rate.sleep()

    def state_update(self, message):

        self.state = message.data

if __name__ == "__main__":
    try:
        bladder_exp()
    except rospy.ROSInterruptException:
        pass
