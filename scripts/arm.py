#!/usr/bin/env python

import rospy
import crazyflie
import time
import math

if __name__ == '__main__':
    rospy.init_node('test_high_level')
    
    cf_prefix = rospy.get_param("~cf_prefix", "cf1")
    tf_prefix = rospy.get_param("~tf_prefix", "/cf1")
    
    should_takeoff = rospy.get_param('~takeoff', False)
    takeoff_height = rospy.get_param('~takeoff_height', 0.2)
    takeoff_duration = rospy.get_param("~takeoff_duration", 2.0)
    sleep_sec_before_takeoff = rospy.get_param('~sleep_sec_before_takeoff', 3.0)

    cf = crazyflie.Crazyflie(cf_prefix, tf_prefix)

    cf.setParam("commander/enHighLevel", 1)
    
    if should_takeoff:
        print("Takeoff in {} seconds".format(sleep_sec_before_takeoff))
        time.sleep(sleep_sec_before_takeoff) 
        cf.takeoff(targetHeight = takeoff_height, duration = takeoff_duration)
        
