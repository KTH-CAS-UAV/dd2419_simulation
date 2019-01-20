#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import re
import os
from subprocess import call
import xml.etree.cElementTree as ET

max_res = 512


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def write_config(output_path, object_type, object_name):
    model = ET.Element("model", version="1.0")
    ET.SubElement(model, "name").text = object_type + '_' + object_name
    ET.SubElement(model, "version").text = '1.0'
    ET.SubElement(model, "sdf",
                  version="1.6").text = 'model.sdf'
    author = ET.SubElement(model, "author")
    ET.SubElement(author, "name").text = 'Daniel Duberg'
    ET.SubElement(author, "email").text = 'dduberg@kth.se'
    ET.SubElement(model, "description")
    tree = ET.ElementTree(model)
    indent(model)
    tree.write(output_path + '/model.config',
               encoding="utf-8", xml_declaration=True)


def write_model(output_path, object_type, object_name, width, height):
    sdf = ET.Element("sdf", version="1.5")

    move_forward = 1e-3
    model = ET.SubElement(sdf, "model", name=object_type + '_' + object_name)
    ET.SubElement(model, "pose", frame="''").text = '0 0 0 0 0 0'
    link = ET.SubElement(model, "link", name="link_0")
    ET.SubElement(link, "pose", frame="''").text = '0 0 0 0 0 0'
    visual = ET.SubElement(link, "visual", name="visual")
    geometry = ET.SubElement(visual, "geometry")
    box = ET.SubElement(geometry, "box")
    ET.SubElement(box, "size").text = str(width) + ' ' + str(height) + ' 1e-5'

    material = ET.SubElement(visual, "material")
    script = ET.SubElement(material, "script")
    ET.SubElement(script, "uri").text = 'model://' + \
        object_type + '_' + object_name + '/materials/scripts'
    ET.SubElement(script, "uri").text = 'model://' + \
        object_type + '_' + object_name + '/materials/textures'
    ET.SubElement(script, "name").text = object_type + \
        '_' + object_name + '/' + object_type

    ET.SubElement(visual, "pose", frame="''").text = '0 0 ' + \
        str(move_forward) + ' 0 0 0'
    ET.SubElement(visual, "cast_shadows").text = '1'
    ET.SubElement(visual, "transparency").text = '0'

    collision = ET.SubElement(link, "collision", name='collision')
    ET.SubElement(collision, "pose",
                  frame="''").text = '0 0 ' + str(move_forward) + ' 0 0 0'
    collision_geometry = ET.SubElement(collision, "geometry")
    collision_box = ET.SubElement(collision_geometry, "box")
    ET.SubElement(collision_box, "size").text = str(
        width) + ' ' + str(height) + ' 1e-5'

    ET.SubElement(model, "static").text = '1'
    ET.SubElement(model, "allow_auto_disable").text = '1'

    # Backside
    visual_backside = ET.SubElement(link, "visual", name="visual_backside")
    ET.SubElement(visual_backside, "pose", frame="''").text = '0 0 0 0 0 0'

    geometry_backside = ET.SubElement(visual_backside, "geometry")
    box_backside = ET.SubElement(geometry_backside, "box")
    ET.SubElement(box_backside, "size").text = str(
        width) + ' ' + str(height) + ' 1e-5'

    material_backside = ET.SubElement(visual_backside, "material")
    ET.SubElement(material_backside, "script").text = 'Gazebo/Grey'

    collision_backside = ET.SubElement(
        link, "collision", name='collision_backside')
    ET.SubElement(collision_backside, "pose", frame="''").text = '0 0 0 0 0 0'
    collision_backside_geometry = ET.SubElement(collision_backside, "geometry")
    collision_backside_box = ET.SubElement(collision_backside_geometry, "box")
    ET.SubElement(collision_backside_box, "size").text = str(
        width) + ' ' + str(height) + ' 1e-5'

    tree = ET.ElementTree(sdf)
    indent(sdf)
    tree.write(output_path + '/model.sdf',
               encoding="utf-8", xml_declaration=True)


def svg_to_model(root_path, object_type, width, height):
    load_dir = root_path + '/svg/' + str(object_type) + 's/'
    save_dir = root_path + '/models/' + str(object_type) + 's/'

    for file in os.listdir(load_dir):
        if len(file) > 4 and file[-4:] == '.svg':
            filename = re.sub('\.svg$', '', file)
            texture_path = save_dir + object_type + '_' + filename + '/materials/textures/'
            script_path = save_dir + object_type + '_' + filename + '/materials/scripts/'
            if not os.path.exists(texture_path):
                os.makedirs(texture_path)
            if not os.path.exists(script_path):
                os.makedirs(script_path)

            full_res_width = str(max_res * min((width / height), 1))
            full_res_height = str(max_res * min((height / width), 1))
            object_res_width = full_res_width
            object_res_height = full_res_height

            background = 'transparent'

            command = 'convert -background ' + background + ' ' + load_dir + file + \
                ' -resize ' + object_res_width + 'x' + object_res_height + ' -background ' + background + ' -gravity center -extent ' + full_res_width + 'x' + full_res_height + ' ' + \
                texture_path + filename
            os.system(command)

            with open(script_path + re.sub('\.svg$', '.material', file), 'w') as f:
                f.write('material ' + object_type + '_' +
                        filename + '/' + object_type + "\n")
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

            write_config(save_dir + object_type + '_' +
                         filename, object_type, filename)
            write_model(save_dir + object_type + '_' + filename,
                        object_type, filename, width, height)
