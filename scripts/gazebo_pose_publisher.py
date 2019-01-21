#!/usr/bin/env python

"""
    @author: Daniel Duberg (dduberg@kth.se)
"""

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Path
from gazebo_msgs.srv import GetModelState
import tf2_ros
import math


def gazebo_pose_publisher():
    pub = rospy.Publisher('/cf1/gazebo_pose', PoseStamped,
                          queue_size=10)
    path_pub = rospy.Publisher('/cf1/gazebo_path', Path, queue_size=10)
    rospy.init_node('gazebo_pose_publisher', anonymous=True)

    path = Path()
    path.header.frame_id = "map"

    br = tf2_ros.TransformBroadcaster()
    t = TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "map"
    t.child_frame_id = "cf1/base_link"

    rospy.wait_for_service('/gazebo/get_model_state')

    rate = rospy.Rate(30)  # 30 Hz
    while not rospy.is_shutdown():
        service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        try:
            resp = service('cf1', '')

            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = rospy.Time.now()
            pose.pose = resp.pose
            pub.publish(pose)

            # TF
            t.transform.translation.x = resp.pose.position.x
            t.transform.translation.y = resp.pose.position.y
            t.transform.translation.z = resp.pose.position.z
            t.transform.rotation.x = resp.pose.orientation.x
            t.transform.rotation.y = resp.pose.orientation.y
            t.transform.rotation.z = resp.pose.orientation.z
            t.transform.rotation.w = resp.pose.orientation.w
            br.sendTransform(t)

            # Add to path
            if len(path.poses) > 0:
                x_enough = math.fabs(
                    pose.pose.position.x - path.poses[-1].pose.position.x) > 0.1
                y_enough = math.fabs(
                    pose.pose.position.y - path.poses[-1].pose.position.y) > 0.1
                z_enough = math.fabs(
                    pose.pose.position.z - path.poses[-1].pose.position.z) > 0.1
                if x_enough or y_enough or z_enough:
                    path.header.stamp = pose.header.stamp
                    path.poses.append(pose)
            else:
                path.header.stamp = pose.header.stamp
                path.poses.append(pose)
            path_pub.publish(path)
        except rospy.ServiceException as exc:
            pass
        # pub.publish(markers)
        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    try:
        gazebo_pose_publisher()
    except rospy.ROSInterruptException:
        pass
