#!/usr/bin/env python

"""
    @author: Daniel Duberg (dduberg@kth.se)
"""

from __future__ import print_function, unicode_literals
import rospkg
import json
import sys
import os
import re
import gates_to_walls
import generate_gazebo_world
import svg_to_model
import usage


def main(argv):
    rospack = rospkg.RosPack()
    # get the file path for dd2419_simulation
    sim_pkg_path = rospack.get_path('dd2419_simulation')
    # get the file path for dd2419_resources
    resource_pkg_path = rospack.get_path('dd2419_resources')

    json_path = resource_pkg_path + '/worlds_json/'

    if len(argv) == 0:
        usage.how_to_use(
            'USAGE: rosrun dd2419_simulation json_to_world.py FILENAME', json_path, '.json')
        exit(1)

    filename = re.sub('\.json$', '', argv[len(argv)-1])

    with open(json_path + filename + '.json') as f:
        data = json.load(f)

        svg_to_model.svg_to_model(
            resource_pkg_path, sim_pkg_path, 'sign', data['roadsign_size'][0], data['roadsign_size'][1])

        svg_to_model.svg_to_model(
            resource_pkg_path, sim_pkg_path, 'marker', data['marker_size'][0], data['marker_size'][1])

        print("Turning gates into walls")
        # 'date =' is not necessary, but easier to read
        data = gates_to_walls.gates_to_walls(data)
        print("")

        save_path = json_path + 'walled/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_path = save_path + 'walled_' + filename + '.json'
        print("Saving walled json world to:", save_path)
        with open(save_path, 'w') as f:
            json.dump(data, f, default=list, indent=2)
        print("")

        print("Generating Gazebo world")
        generate_gazebo_world.generate_world(
            sim_pkg_path + '/worlds/' +
            re.sub('\.world$', '', filename) + '.world', data, sim_pkg_path)
        print("")


if __name__ == "__main__":
    main(sys.argv[1:])
