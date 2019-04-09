#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64,String


class state_params():
    def __init__(self):

        self.state_pub = rospy.Publisher('state', String, queue_size=10)

        self.sub = rospy.Subscriber('depth_publish', Float64, self.depth_update)
        self.depth = 0
        rospy.init_node("state_node")
        self.rate = rospy.Rate(2)

        self.state_publisher()

    def state_publisher(self):

        state = 'descend'

        while not rospy.is_shutdown():

            if self.depth < -2.7 and state == 'descend':
                state = 'ascend'
            elif self.depth >-0.4 and state == 'ascend':
                state = 'descend'

            self.state_pub.publish(state)

            rospy.loginfo("Glider depth is %s m and state is %s" % (self.depth, state))

            self.rate.sleep()

    def depth_update(self, message):

        self.depth = message.data

if __name__ == "__main__":
    try:
        state_params()
    except rospy.ROSInterruptException:
        pass
