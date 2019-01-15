#!/usr/bin/env python

import rospkg
import json
import sys
import re
import generate_gazebo_world
import generate_rviz_world


def main(argv):
    if len(argv) == 0:
        print("You have to input the json file")
        exit(1)

    rospack = rospkg.RosPack()
    # get the file path for dd2419_simulation
    sim_pkg_path = rospack.get_path('dd2419_simulation')

    filename = re.sub('\.json$', '', argv[0])

    with open(sim_pkg_path + '/worlds_json/' + filename + '.json') as f:
        data = json.load(f)

        generate_gazebo_world.generate_world(
            sim_pkg_path + '/worlds/' + filename + '.world', data)

        generate_rviz_world.generate_world(
            sim_pkg_path + '/worlds_rviz/' + filename + '.data', data)


if __name__ == "__main__":
    main(sys.argv[1:])
