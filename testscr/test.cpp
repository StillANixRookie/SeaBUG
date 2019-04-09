#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <stdlib.h>

int main(int argc, char**argv){
  ros::init(argc, argv, "publish_imu");
  ros::NodeHandle nh;

  ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("imu", 100);

  srand(time(0));

  ros::Rate rate(2);
  while(ros::ok()){
    geometry_msgs::Twist msg;
    msg.linear.x = imu.a[0]
    msg.linear.y = imu.a[1]
    msg.linear.z = imu.a[2]
    msg.angular.x = imu.g[0]
    msg.angular.y = imu.g[1]
    msg.angular.z = imu.g[2]

    pub.publish(msg);

    rate.sleep();
  }
}
