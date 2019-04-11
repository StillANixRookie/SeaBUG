import rospy
from std_msgs.msg import Float64
import smbus
import time

#!/usr/bin/env python

#simplePingExample.py
from brping import Ping1D
import time
import argparse

from builtins import input

##Parse Command line options
############################
#parser = argparse.ArgumentParser(description="Ping python library example.")
#parser.add_argument('--device', action="store", type=str, default="/dev/ttyUSB0", help="Ping device port.")
#parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate.")
#args = parser.parse_args()

#Make a new Ping
myPing = Ping1D("/dev/ttyUSB0", 115200)
if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

myPing.set_speed_of_sound(340000)

print("------------------------------------")
print("Starting Ping..")
print("Press CTRL+C to exit")
print("------------------------------------")

#input("Press Enter to continue...")

# Read and print distance measurements with confidence
#while True:
#    data = myPing.get_distance()
#    if data:
#        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
#    else:
#        print("Failed to get distance data")
#    time.sleep(0.1)

def range_publisher():
    pub_dist = rospy.Publisher('Range', Float64, queue_size=10)
    pub_conf = rospy.Publisher('Confidence', Float64, queue_size=10)

    rate = rospy.Rate(10)

    range_to_publish = Float64()
    conf_to_publish = Float64()

    while not rospy.is_shutdown():
        reading = myPing.get_distance()
        range = reading["distance"]
        conf = reading["confidence"]
        time.sleep(0.1)

        range_to_publish.data = range
        conf_to_publish.data = conf

        pub_dist.publish(range_to_publish)
        pub_conf.publish(conf_to_publish)

#        rospy.loginfo(range_to_publish)

        rate.sleep()

if __name__ == "__main__":
    rospy.init_node("range_publisher")
    range_publisher()
