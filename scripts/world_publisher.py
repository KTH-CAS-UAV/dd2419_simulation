#!/usr/bin/env python

"""
    @author: Daniel Duberg (dduberg@kth.se)
"""

import rospy
import json
import gates_to_walls
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import tf
import math


def add_ground(markers, data):
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "ground"
    marker.id = 0
    marker.type = Marker.CUBE
    marker.action = Marker.ADD
    marker.pose.position.x = (
        data['airspace']['min'][0] + data['airspace']['max'][0]) / 2
    marker.pose.position.y = (
        data['airspace']['min'][1] + data['airspace']['max'][1]) / 2
    marker.pose.position.z = -1e-3
    marker.pose.orientation.x = 0
    marker.pose.orientation.y = 0
    marker.pose.orientation.z = 0
    marker.pose.orientation.w = 1
    marker.scale.x = data['airspace']['max'][0] - data['airspace']['min'][0]
    marker.scale.y = data['airspace']['max'][1] - data['airspace']['min'][1]
    marker.scale.z = 1e-4
    marker.color.a = 1.0
    marker.color.r = 0.8
    marker.color.g = 0.8
    marker.color.b = 0.8
    markers.markers.append(marker)


def add_airspace(markers, data):
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "airspace"
    marker.id = 0
    marker.type = Marker.CUBE
    marker.action = Marker.ADD
    marker.pose.position.x = (
        data['airspace']['min'][0] + data['airspace']['max'][0]) / 2
    marker.pose.position.y = (
        data['airspace']['min'][1] + data['airspace']['max'][1]) / 2
    marker.pose.position.z = ((
        data['airspace']['min'][2] + data['airspace']['max'][2]) / 2)
    marker.pose.orientation.x = 0
    marker.pose.orientation.y = 0
    marker.pose.orientation.z = 0
    marker.pose.orientation.w = 1
    marker.scale.x = data['airspace']['max'][0] - data['airspace']['min'][0]
    marker.scale.y = data['airspace']['max'][1] - data['airspace']['min'][1]
    marker.scale.z = data['airspace']['max'][2] - data['airspace']['min'][2]
    marker.color.a = 0.2
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    markers.markers.append(marker)

    marker_text = Marker()
    marker_text.header.frame_id = "map"
    marker_text.header.stamp = rospy.Time.now()
    marker_text.ns = "airspace_text"
    marker_text.id = 0
    marker_text.type = Marker.TEXT_VIEW_FACING
    marker_text.text = 'airspace'
    marker_text.action = Marker.ADD
    marker_text.pose.position.x = (
        data['airspace']['min'][0] + data['airspace']['max'][0]) / 2
    marker_text.pose.position.y = (
        data['airspace']['min'][1] + data['airspace']['max'][1]) / 2
    marker_text.pose.position.z = (data['airspace']['min'][2] + data['airspace']['max'][2]) + (
        data['airspace']['min'][2] + data['airspace']['max'][2])/2
    marker_text.pose.orientation.x = 0
    marker_text.pose.orientation.y = 0
    marker_text.pose.orientation.z = 0
    marker_text.pose.orientation.w = 1
    marker_text.scale.x = data['airspace']['max'][0] - \
        data['airspace']['min'][0]
    marker_text.scale.y = data['airspace']['max'][1] - \
        data['airspace']['min'][1]
    marker_text.scale.z = data['airspace']['max'][2] - \
        data['airspace']['min'][2]
    marker_text.color.a = 1.0
    marker_text.color.r = 1.0
    marker_text.color.g = 1.0
    marker_text.color.b = 1.0
    markers.markers.append(marker_text)


def add_markers(markers, data):
    for elem in data['markers']:
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "markers"
        marker.id = elem['id']
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.position.x = elem['pose']['position'][0]
        marker.pose.position.y = elem['pose']['position'][1]
        marker.pose.position.z = elem['pose']['position'][2]
        quaternion = tf.transformations.quaternion_from_euler(
            math.radians(elem['pose']['orientation'][0] - 90), math.radians(
                elem['pose']['orientation'][1]), math.radians(
                    elem['pose']['orientation'][2]))
        marker.pose.orientation.x = quaternion[0]
        marker.pose.orientation.y = quaternion[1]
        marker.pose.orientation.z = quaternion[2]
        marker.pose.orientation.w = quaternion[3]
        marker.scale.x = data['marker_size'][0]
        marker.scale.y = data['marker_size'][1]
        marker.scale.z = 1e-5
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        markers.markers.append(marker)

        marker_text = Marker()
        marker_text.header.frame_id = "map"
        marker_text.header.stamp = rospy.Time.now()
        marker_text.ns = "markers_text"
        marker_text.id = elem['id']
        marker_text.type = Marker.TEXT_VIEW_FACING
        marker_text.text = str(elem['id'])
        marker_text.action = Marker.ADD
        marker_text.pose.position.x = elem['pose']['position'][0]
        marker_text.pose.position.y = elem['pose']['position'][1]
        marker_text.pose.position.z = elem['pose']['position'][2] + (
            max(data['marker_size'][0], data['marker_size'][1]))
        quaternion = tf.transformations.quaternion_from_euler(
            math.radians(elem['pose']['orientation'][0] - 90), math.radians(
                elem['pose']['orientation'][1]), math.radians(
                    elem['pose']['orientation'][2]))
        marker_text.pose.orientation.x = quaternion[0]
        marker_text.pose.orientation.y = quaternion[1]
        marker_text.pose.orientation.z = quaternion[2]
        marker_text.pose.orientation.w = quaternion[3]
        marker_text.scale.x = data['marker_size'][0]
        marker_text.scale.y = data['marker_size'][1]
        marker_text.scale.z = 0.1
        marker_text.color.a = 1.0
        marker_text.color.r = 1.0
        marker_text.color.g = 1.0
        marker_text.color.b = 1.0
        markers.markers.append(marker_text)


def add_signs(markers, data):
    for idx, elem in enumerate(data['roadsigns']):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "signs"
        marker.id = idx
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.position.x = elem['pose']['position'][0]
        marker.pose.position.y = elem['pose']['position'][1]
        marker.pose.position.z = elem['pose']['position'][2]
        quaternion = tf.transformations.quaternion_from_euler(
            math.radians(elem['pose']['orientation'][0] - 90), math.radians(
                elem['pose']['orientation'][1]), math.radians(
                    elem['pose']['orientation'][2]))
        marker.pose.orientation.x = quaternion[0]
        marker.pose.orientation.y = quaternion[1]
        marker.pose.orientation.z = quaternion[2]
        marker.pose.orientation.w = quaternion[3]
        marker.scale.x = data['roadsign_size'][0]
        marker.scale.y = data['roadsign_size'][1]
        marker.scale.z = 1e-5
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        markers.markers.append(marker)

        marker_text = Marker()
        marker_text.header.frame_id = "map"
        marker_text.header.stamp = rospy.Time.now()
        marker_text.ns = "signs_text"
        marker_text.id = idx
        marker_text.type = Marker.TEXT_VIEW_FACING
        marker_text.text = str(elem['sign'])
        marker_text.action = Marker.ADD
        marker_text.pose.position.x = elem['pose']['position'][0]
        marker_text.pose.position.y = elem['pose']['position'][1]
        marker_text.pose.position.z = elem['pose']['position'][2] + (
            max(data['roadsign_size'][0], data['roadsign_size'][1]))
        quaternion = tf.transformations.quaternion_from_euler(
            math.radians(elem['pose']['orientation'][0] - 90), math.radians(
                elem['pose']['orientation'][1]), math.radians(
                    elem['pose']['orientation'][2]))
        marker_text.pose.orientation.x = quaternion[0]
        marker_text.pose.orientation.y = quaternion[1]
        marker_text.pose.orientation.z = quaternion[2]
        marker_text.pose.orientation.w = quaternion[3]
        marker_text.scale.x = data['roadsign_size'][0]
        marker_text.scale.y = data['roadsign_size'][1]
        marker_text.scale.z = 0.1
        marker_text.color.a = 1.0
        marker_text.color.r = 1.0
        marker_text.color.g = 1.0
        marker_text.color.b = 1.0
        markers.markers.append(marker_text)


def add_walls(markers, data):
    for idx, elem in enumerate(data['walls']):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        if 'gate' in elem:
            marker.ns = "gates"
        else:
            marker.ns = "walls"
        marker.id = idx
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.position.x = (
            elem['plane']['stop'][0] + elem['plane']['start'][0])/2
        marker.pose.position.y = (
            elem['plane']['stop'][1] + elem['plane']['start'][1])/2
        marker.pose.position.z = (
            elem['plane']['stop'][2] + elem['plane']['start'][2])/2
        quaternion = tf.transformations.quaternion_from_euler(math.radians(90), 0, math.atan2(
            elem['plane']['stop'][1] - elem['plane']['start'][1], elem['plane']['stop'][0] - elem['plane']['start'][0]) + math.radians(90))
        marker.pose.orientation.x = quaternion[0]
        marker.pose.orientation.y = quaternion[1]
        marker.pose.orientation.z = quaternion[2]
        marker.pose.orientation.w = quaternion[3]
        marker.scale.x = 1e-5
        marker.scale.y = math.fabs(
            (elem['plane']['stop'][2] - elem['plane']['start'][2]))
        marker.scale.z = math.hypot(elem['plane']['stop'][0] - elem['plane']['start'][0], elem['plane']
                                    ['stop'][1] - elem['plane']['start'][1])
        marker.color.a = 1.0
        if 'gate' in elem:
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 1.0
        else:
            marker.color.r = 0.7
            marker.color.g = 0.4
            marker.color.b = 0.0
        markers.markers.append(marker)

        if 'gate' in elem:
            # Backside
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = rospy.Time.now()
            marker.ns = "gates"
            marker.id = idx + 1000
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose.position.x = (
                elem['plane']['stop'][0] + elem['plane']['start'][0])/2 + 1e-2 * math.cos(math.atan2(
                    elem['plane']['stop'][1] - elem['plane']['start'][1], elem['plane']['stop'][0] - elem['plane']['start'][0]) + math.radians(90))
            marker.pose.position.y = (
                elem['plane']['stop'][1] + elem['plane']['start'][1])/2 + 1e-2 * math.sin(math.atan2(
                    elem['plane']['stop'][1] - elem['plane']['start'][1], elem['plane']['stop'][0] - elem['plane']['start'][0]) + math.radians(90))
            marker.pose.position.z = (
                elem['plane']['stop'][2] + elem['plane']['start'][2])/2
            quaternion = tf.transformations.quaternion_from_euler(math.radians(90), 0, math.atan2(
                elem['plane']['stop'][1] - elem['plane']['start'][1], elem['plane']['stop'][0] - elem['plane']['start'][0]) + math.radians(90))
            marker.pose.orientation.x = quaternion[0]
            marker.pose.orientation.y = quaternion[1]
            marker.pose.orientation.z = quaternion[2]
            marker.pose.orientation.w = quaternion[3]
            marker.scale.x = 1e-5
            marker.scale.y = math.fabs(
                (elem['plane']['stop'][2] - elem['plane']['start'][2]))
            marker.scale.z = math.hypot(elem['plane']['stop'][0] - elem['plane']['start'][0], elem['plane']
                                        ['stop'][1] - elem['plane']['start'][1])
            marker.color.a = 1.0
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            markers.markers.append(marker)

            # Text
            marker_text = Marker()
            marker_text.header.frame_id = "map"
            marker_text.header.stamp = rospy.Time.now()
            marker_text.ns = "gates_text"
            marker_text.id = elem['gate']
            marker_text.type = Marker.TEXT_VIEW_FACING
            marker_text.text = 'gate ' + str(elem['gate'])
            marker_text.action = Marker.ADD
            marker_text.pose.position.x = (
                elem['plane']['stop'][0] + elem['plane']['start'][0])/2
            marker_text.pose.position.y = (
                elem['plane']['stop'][1] + elem['plane']['start'][1])/2
            marker_text.pose.position.z = (
                elem['plane']['stop'][2] + elem['plane']['start'][2])
            quaternion = tf.transformations.quaternion_from_euler(math.radians(90), 0, math.atan2(
                elem['plane']['stop'][1] - elem['plane']['start'][1], elem['plane']['stop'][0] - elem['plane']['start'][0]))
            marker_text.pose.orientation.x = quaternion[0]
            marker_text.pose.orientation.y = quaternion[1]
            marker_text.pose.orientation.z = quaternion[2]
            marker_text.pose.orientation.w = quaternion[3]
            marker_text.scale.x = math.hypot(elem['plane']['stop'][0] - elem['plane']['start'][0], elem['plane']
                                             ['stop'][1] - elem['plane']['start'][1])
            marker_text.scale.y = math.fabs(
                (elem['plane']['stop'][2] - elem['plane']['start'][2]))
            marker_text.scale.z = 0.1
            marker_text.color.a = 1.0
            marker_text.color.r = 1.0
            marker_text.color.g = 1.0
            marker_text.color.b = 1.0
            markers.markers.append(marker_text)


def world_publisher():
    pub = rospy.Publisher('world', MarkerArray, queue_size=10, latch=True)
    rospy.init_node('world_publisher', anonymous=True)

    markers = MarkerArray()

    with open(rospy.get_param("~json_file")) as f:
        data = json.load(f)

        # 'date =' is not necessary, but easier to read
        data = gates_to_walls.gates_to_walls(data)

        add_ground(markers, data)

        add_airspace(markers, data)

        add_markers(markers, data)

        add_signs(markers, data)

        add_walls(markers, data)

    rate = rospy.Rate(1)  # 1 Hz
    while not rospy.is_shutdown():
        pub.publish(markers)
        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    try:
        world_publisher()
    except rospy.ROSInterruptException:
        pass
