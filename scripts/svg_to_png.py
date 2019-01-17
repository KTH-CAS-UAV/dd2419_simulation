#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import re
import os
from subprocess import call

max_res = 512


def svg_to_png(path, object_type, width, height):
    load_dir = path + '/' + str(object_type) + '/original/'
    save_dir = path + '/' + str(object_type) + '/' + \
        str(width) + 'x' + str(height) + '/'
    if not os.path.exists(save_dir + 'textures/'):
        os.makedirs(save_dir + 'textures/')
    if not os.path.exists(save_dir + 'scripts/'):
        os.makedirs(save_dir + 'scripts/')
    for file in os.listdir(load_dir):
        if len(file) > 4 and file[-4:] == '.svg':
            res_width = str(max_res * min((width / height), 1))
            res_height = str(max_res * min((height / width), 1))
            command = 'convert -background transparent ' + load_dir + file + \
                ' -resize ' + res_width + 'x' + res_height + ' -background transparent -gravity center -extent ' + res_width + 'x' + res_height + ' ' + \
                save_dir + 'textures/' + re.sub('\.svg$', '.png', file)
            os.system(command)

            with open(save_dir + 'scripts/' + re.sub('\.svg$', '.material', file), 'w') as f:
                f.write('material ' + object_type[:-1] + '_' +
                        re.sub('\.svg$', '', file) + '/' + object_type[:-1] + "\n")
                f.write('{\n')
                f.write('  technique\n')
                f.write('  {\n')
                f.write('    pass\n')
                f.write('    {\n')
                f.write('      texture_unit\n')
                f.write('      {\n')
                f.write('        texture ' +
                        re.sub('\.svg$', '.png', file) + '\n')
                f.write('      }\n')
                f.write('    }\n')
                f.write('  }\n')
                f.write('}\n')


def generate_signs(path, width, height):
    svg_to_png(path, 'signs', width, height)


def generate_markers(path, width, height):
    svg_to_png(path, 'markers', width, height)
