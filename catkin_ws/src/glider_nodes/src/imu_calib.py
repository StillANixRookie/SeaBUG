#!/usr/bin/env python

from __future__ import division

import rospy
import tf
from std_msgs.msg import Float32
from geometry_msgs.msg import Vector3, Quaternion
from sensor_msgs.msg import Imu, MagneticField
import math

from imu_utils import ImuReader

IMU_BUS = 1

# minIMU without the jumper wired
LGD = 0x6b #Device I2C slave address
LSM = 0x1d #Device I2C slave address

# minIMU with the jumper wired
# LGD = 0x6a #Device I2C slave address
# LSM = 0x1e #Device I2C slave address

def heading_publisher():

    #rate = rospy.Rate(rospy.get_param("config/rate"))
    rate = rospy.Rate(100)
    #calib = rospy.get_param('calibration/compass')
    use_heading_comp = 5# rospy.get_param('heading/compensation')
    offset_true_north = 2# rospy.get_param('heading/offset_true_north')

    imudata = Imu()
    XOFFSET =  -1102 #calib['XOFFSET']
    YOFFSET =  348 #calib['YOFFSET']
    ZOFFSET =  2028.56 #calib['ZOFFSET']
    XSCALE =  1990# calib['XSCALE']
    YSCALE =  2174 #calib['YSCALE']
    ZSCALE =  389.266# calib['ZSCALE']


    imu = ImuReader(IMU_BUS, LSM, LGD)
    imu.check_status()
    imu.configure_for_reading()

    while not rospy.is_shutdown():
        #Read data from the chips ----------------------
        rate.sleep()
        magx, magy, magz = imu.read_mag_field()
        # * 16 to nanoTesla, /1e9 to Tesla
        MagX = magx * 16 / 1e9
        MagY = magy * 16 / 1e9
        MagZ = magz * 16 / 1e9


        accx, accy, accz = imu.read_acceleration()
        # * 0.061 to g, * 9.8 to m/s^2
        AccX = accx * 0.061 * 9.8
        AccY = accy * 0.061 * 9.8
        AccZ = accz * 0.061 * 9.8

        pitch = math.atan2(AccX, math.sqrt(AccY**2 + AccZ**2))
        roll = math.atan2(-AccY, -AccZ)

        gyrox, gyroy, gyroz = imu.read_gyro()

        # * 8.75 to mdeg/s, /1000 to deg/s, then convert to radians/s
        GyroX = gyrox * 8.75/1000 * math.pi /180
        GyroY = gyroy * 8.75/1000 * math.pi /180
        GyroZ = gyroz * 8.75/1000 * math.pi /180


        # calibration
        MagX = (MagX - XOFFSET) / XSCALE
        MagY = (MagY - YOFFSET) / YSCALE
        MagZ = (MagZ - ZOFFSET) / ZSCALE

        mag_field_pub.publish(Vector3(MagX, MagY, MagZ))
        acc_pub.publish(Vector3(AccX, AccY, AccZ))

        heading = math.degrees(math.atan2(-MagY, MagX))
        heading = (heading + offset_true_north) % 360

        imu_raw_msg = Imu()
        imu_raw_msg.header.stamp = rospy.Time.now()
        imu_raw_msg.header.frame_id = "sailrobot"
        [imu_raw_msg.orientation.x,
         imu_raw_msg.orientation.y,
         imu_raw_msg.orientation.z,
         imu_raw_msg.orientation.w]= tf.transformations.quaternion_from_euler(roll, pitch, math.radians(heading))
        imu_raw_msg.angular_velocity = Vector3(GyroX, GyroY, GyroZ)
        imu_raw_msg.linear_acceleration = Vector3(AccX, AccY, AccZ)
        imu_raw_pub.publish(imu_raw_msg)


        mag_raw_msg = MagneticField()
        mag_raw_msg.header.stamp = rospy.Time.now()
        mag_raw_msg.magnetic_field = Vector3(MagX, MagY, MagZ)
        mag_raw_pub.publish(mag_raw_msg)



        MagX_comp = (MagX*math.cos(pitch)) + (MagZ*math.sin(pitch))
        MagY_comp = (MagX*math.sin(roll)*math.sin(pitch)) +\
                    (MagY*math.cos(roll)) - (MagZ*math.sin(roll)*math.cos(pitch))

        # We don't calculate a compensated Z field, so publish it as 0
        mag_field_comp_pub.publish(Vector3(MagX_comp, MagY_comp, 0))

        heading_comp = math.degrees(math.atan2(-MagY_comp, MagX_comp))
        heading_comp = (heading_comp + offset_true_north) % 360

        imudata.linear_acceleration.x = AccX
        imudata.linear_acceleration.y = - AccY
        imudata.linear_acceleration.z = - AccZ # convert from IMU to base frame

        imudata.angular_velocity.x = gyrox
        imudata.angular_velocity.y = - gyroy
        imudata.angular_velocity.z = - gyroz
        # publish either the compensated heading or the raw one depending on the parameter
        if use_heading_comp:
            heading_pub.publish(heading_comp)
        else:
            heading_pub.publish(heading)

        pitch_pub.publish(math.degrees(pitch))
        roll_pub.publish(math.degrees(roll))
        imu_pub.publish(imudata)

if __name__ == '__main__':
    try:
        mag_field_pub = rospy.Publisher('minimu/mag', Vector3, queue_size=10)
        imu_raw_pub = rospy.Publisher('minimu/data_raw', Imu, queue_size=10)
        mag_raw_pub = rospy.Publisher('minimu/mag', MagneticField, queue_size=10)
        mag_field_comp_pub = rospy.Publisher('minimu/mag_field_xy_compensated', Vector3, queue_size=10)
        acc_pub = rospy.Publisher('minimu/acceleration', Vector3, queue_size=10)
        heading_pub = rospy.Publisher('minimu/heading', Float32, queue_size=10)
        pitch_pub =  rospy.Publisher('minimu/pitch', Float32, queue_size=10)
        roll_pub = rospy.Publisher('minimu/roll', Float32, queue_size=10)
        imu_pub = rospy.Publisher('minimu/data', Imu, queue_size=10)

        rospy.init_node("publish_heading_data", anonymous=True)
        heading_publisher()
    except rospy.ROSInterruptException:
        pass
