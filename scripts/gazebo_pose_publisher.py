#!/usr/bin/env python

"""
    @author: Daniel Duberg (dduberg@kth.se)
"""

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TransformStamped
from gazebo_msgs.srv import GetModelState
import tf2_ros
import math


def gazebo_pose_publisher():
    pub = rospy.Publisher('/cf1/pose', PoseStamped,
                          queue_size=10)
    rospy.init_node('gazebo_pose_publisher', anonymous=True)

    br = tf2_ros.TransformBroadcaster()
    t = TransformStamped()
    t.header.frame_id = "cf1/odom"
    t.child_frame_id = "cf1/base_link"

    rospy.wait_for_service('/gazebo/get_model_state')

    rate = rospy.Rate(30)  # 30 Hz
    while not rospy.is_shutdown():
        service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        try:
            resp = service('cf1', '')

            pose = PoseStamped()
            pose.header.frame_id = "cf1/odom"
            pose.header.stamp = rospy.Time.now()
            pose.pose = resp.pose
            pub.publish(pose)

            # TF
            t.header.stamp = rospy.Time.now()

            t.transform.translation.x = pose.pose.position.x
            t.transform.translation.y = pose.pose.position.y
            t.transform.translation.z = pose.pose.position.z
            t.transform.rotation.x = pose.pose.orientation.x
            t.transform.rotation.y = pose.pose.orientation.y
            t.transform.rotation.z = pose.pose.orientation.z
            t.transform.rotation.w = pose.pose.orientation.w
            br.sendTransform(t)
        except rospy.ServiceException as exc:
            pass
        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    try:
        gazebo_pose_publisher()
    except rospy.ROSInterruptException:
        pass
