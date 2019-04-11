#!/usr/bin/python
import ms5837
import time
import rospy
from std_msgs.msg import Float64

sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)
#sensor = ms5837.MS5837_30BA(0) # Specify I2C bus
#sensor = ms5837.MS5837_02BA()
#sensor = ms5837.MS5837_02BA(0)
#sensor = ms5837.MS5837(model=ms5837.MS5837_MODEL_30BA, bus=0) # Specify model and bus

# We must initialize the sensor before reading it
if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print "Sensor read failed!"
    exit(1)

time.sleep(5)

def depth_publisher():
    pub_depth = rospy.Publisher('Depth', Float64, queue_size=10)

    rate = rospy.Rate(10)

    depth_to_publish = Float64()
    
    while not rospy.is_shutdown():
    
        if sensor.read():
            depth = sensor.depth() 
        else:
            print "Sensor read failed!"
            exit(1)

        depth_to_publish.data = depth

        pub_depth.publish(depth_to_publish)

        rate.sleep()

if __name__ == "__main__":
    rospy.init_node("depth_publisher")
    depth_publisher()
