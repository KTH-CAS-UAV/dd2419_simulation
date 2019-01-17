#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import rospkg
import json
import sys
import re
import gates_to_walls
import generate_gazebo_world
import svg_to_png


def main(argv):
    if len(argv) == 0:
        print("You have to input the json file")
        exit(1)

    filename = re.sub('\.json$', '', argv[len(argv)-1])

    saved_walled = False
    for arg in argv:
        if arg == "-w" or arg == "--save_walled":
            saved_walled = True
        elif arg == "-h" or arg == "--help":
            print("")
            print(
                "rosrun dd2419_simulation json_to_world.py [OPTIONS] filename")
            print("")
            print("OPTIONS")
            print("  -h, --help:         Show this message")
            print("  -w, --save_walled:  Saved a file where gates have become walls")
            exit(0)

    rospack = rospkg.RosPack()
    # get the file path for dd2419_simulation
    sim_pkg_path = rospack.get_path('dd2419_simulation')

    with open(sim_pkg_path + '/worlds_json/' + filename + '.json') as f:
        data = json.load(f)

        svg_to_png.generate_signs(
            sim_pkg_path, data['roadsign_size'][0], data['roadsign_size'][1])

        svg_to_png.generate_markers(
            sim_pkg_path, data['marker_size'][0], data['marker_size'][1])

        print("Turning gates into walls")
        # 'date =' is not necessary, but easier to read
        data = gates_to_walls.gates_to_walls(data)
        print("")

        if saved_walled:
            save_path = sim_pkg_path + '/worlds_json/walled_' + filename + '.json'
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
