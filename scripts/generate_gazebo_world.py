#!/usr/bin/env python

import xml.etree.cElementTree as ET
import math


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


def generate_world(save_path, data):
    sdf = ET.Element("sdf", version="1.5")

    world = ET.SubElement(sdf, "world", name="default")

    # Add sun
    ET.SubElement(ET.SubElement(world, "include"), "uri").text = "model://sun"

    # Add ground plane
    ground_include = ET.SubElement(world, "include")
    ET.SubElement(ground_include, "uri").text = "model://ground_plane"
    ET.SubElement(ground_include, "pose").text = "0 0 -0.001 0 0 0"

    # Add airspace from json file
    airspace_model = ET.SubElement(world, "model", name="airspace")
    airspace_link = ET.SubElement(
        airspace_model, "link", name="link_0")
    ET.SubElement(
        airspace_link, "pose", frame="").text = str((data['airspace']['min'][0] + data['airspace']['max'][0]) / 2) + ' ' + str((data['airspace']['min'][1] + data['airspace']['max'][1]) / 2) + ' ' + str((data['airspace']['min'][2] + data['airspace']['max'][2]) / 2) + ' 0 0 0'
    ET.SubElement(airspace_link, "gravity").text = "0"
    ET.SubElement(airspace_link, "self_collide").text = "0"
    ET.SubElement(airspace_link, "kinematic").text = "1"

    airspace_visual = ET.SubElement(
        airspace_link, "visual", name="airspace_visual")
    ET.SubElement(
        airspace_visual, "pose", frame="").text = '0 0 0 0 0 0'

    airspace_geometry = ET.SubElement(airspace_visual, "geometry")
    airspace_box = ET.SubElement(airspace_geometry, "box")
    ET.SubElement(airspace_box, "size").text = str(
        data['airspace']['max'][0] - data['airspace']['min'][0]) + ' ' + str(
        data['airspace']['max'][1] - data['airspace']['min'][1]) + ' ' + str(
        data['airspace']['max'][2] - data['airspace']['min'][2])

    airspace_material = ET.SubElement(airspace_visual, "material")
    airspace_script = ET.SubElement(airspace_material, "script")
    ET.SubElement(
        airspace_script, "uri").text = 'file://media/materials/scripts/gazebo.material'
    ET.SubElement(
        airspace_script, "name").text = 'Gazebo/DarkOrangeTransparentOverlay'

    ET.SubElement(airspace_visual, "cast_shadows").text = '0'
    ET.SubElement(airspace_visual, "transparency").text = '0.85'

    # Add markers from json file
    for elem in data['markers']:
        elem['pose']['orientation'][0] = elem['pose']['orientation'][0] - 90
        include = ET.SubElement(world, "include")
        ET.SubElement(include, "uri").text = "model://aruco_visual_marker_" + \
            str(elem['id']) + "_pad"
        ET.SubElement(include, "pose").text = ' '.join(str(
            e) for e in elem['pose']['position']) + ' ' + ' '.join(str(
                math.radians(e)) for e in elem['pose']['orientation'])

    # Add gates from json file
    # for elem in data['gates']:
    #     elem['heading'] = elem['heading'] + 90
    #     include = ET.SubElement(world, "include")
    #     ET.SubElement(include, "uri").text = "model://gate"
    #     ET.SubElement(include, "pose").text = ' '.join(str(
    #         e) for e in elem['position']) + ' 0 0 ' + str(math.radians(elem['heading']))

    # Add walls from json file
    for idx, elem in enumerate(data['walls']):
        model = ET.SubElement(world, "model", name='wall_' + str(idx))
        link = ET.SubElement(model, "link", name="link_0")
        # TODO: Fix
        ET.SubElement(link, "pose", frame="").text = str((elem['plane']['stop'][0] + elem['plane']['start'][0])/2) + ' ' + str((elem['plane']['stop'][1] + elem['plane']['start'][1])/2) + ' ' + str((elem['plane']['stop'][2] + elem['plane']['start'][2])/2) + ' 0 0 ' + \
            str(math.atan2(elem['plane']['stop'][1] - elem['plane']['start']
                           [1], elem['plane']['stop'][0] - elem['plane']['start'][0]))
        ET.SubElement(link, "gravity").text = "0"
        ET.SubElement(link, "self_collide").text = "0"
        ET.SubElement(link, "kinematic").text = "1"

        visual = ET.SubElement(
            link, "visual", name='wall_' + str(idx) + '_visual')
        ET.SubElement(visual, "pose",
                      frame="").text = '0 0 0 0 0 0'  # TODO: Fix
        geometry = ET.SubElement(visual, "geometry")
        box = ET.SubElement(geometry, "box")
        ET.SubElement(box, "size").text = str(math.hypot(elem['plane']['stop'][0] - elem['plane']['start'][0], elem['plane']
                                                         ['stop'][1] - elem['plane']['start'][1])) + ' 0.02 ' + str(math.fabs((elem['plane']['stop'][2] - elem['plane']['start'][2])))
        # plane = ET.SubElement(geometry, "plane")
        # ET.SubElement(plane, "normal").text = '0 0 1'
        # ET.SubElement(plane, "size").text = str(
        #     math.hypot(elem['plane']['stop'][0] - elem['plane']['start'][0], elem['plane']['stop'][1] - elem['plane']['start'][1])) + ' ' + str(math.fabs((elem['plane']['stop'][2] - elem['plane']['start'][2])))

        material = ET.SubElement(visual, "material")
        script = ET.SubElement(material, "script")
        ET.SubElement(
            script, "uri").text = 'file://media/materials/scripts/gazebo.material'
        ET.SubElement(
            script, "name").text = 'Gazebo/DarkOrangeTransparentOverlay'

        ET.SubElement(visual, "cast_shadows").text = '1'
        ET.SubElement(visual, "transparency").text = '0'

        collision = ET.SubElement(
            link, "collision", name='wall_' + str(idx) + '_collision')
        ET.SubElement(collision, "pose",
                      frame="").text = '0 0 0 0 0 0'  # TODO: Fix
        collision_geometry = ET.SubElement(collision, "geometry")
        collision_box = ET.SubElement(collision_geometry, "box")
        ET.SubElement(collision_box, "size").text = str(math.hypot(elem['plane']['stop'][0] - elem['plane']['start'][0], elem['plane']
                                                                   ['stop'][1] - elem['plane']['start'][1])) + ' 0.02 ' + str(math.fabs((elem['plane']['stop'][2] - elem['plane']['start'][2])))

    # Add signs from json file
    for elem in data['roadsigns']:
        elem['pose']['orientation'][0] = elem['pose']['orientation'][0] - 90
        include = ET.SubElement(world, "include")
        ET.SubElement(include, "uri").text = "model://sign_" + \
            str(elem['sign'])
        ET.SubElement(include, "pose").text = ' '.join(str(
            e) for e in elem['pose']['position']) + ' ' + ' '.join(str(
                math.radians(e)) for e in elem['pose']['orientation'])

    # Add Crazyflie
    # crazyflie_include = ET.SubElement(world, "include")
    # ET.SubElement(crazyflie_include, "uri").text = "model://crazyflie"
    # ET.SubElement(crazyflie_include, "pose").text = "0 0 0.03 0 0 0"

    # Add physics properties
    physics = ET.SubElement(
        world, "physics", name='default_physics', default='0', type='ode')
    ET.SubElement(physics, "gravity").text = "0 0 -9.8066"

    ode = ET.SubElement(physics, "ode")

    solver = ET.SubElement(ode, "solver")
    ET.SubElement(solver, "type").text = "quick"
    ET.SubElement(solver, "iters").text = "20"
    ET.SubElement(solver, "sor").text = "1.3"
    ET.SubElement(solver, "use_dynamic_moi_rescaling").text = "0"

    constraints = ET.SubElement(ode, "constraints")
    ET.SubElement(constraints, "cfm").text = "0"
    ET.SubElement(constraints, "erp").text = "0.2"
    ET.SubElement(constraints, "contact_max_correcting_vel").text = "100"
    ET.SubElement(constraints, "contact_surface_layer").text = "0.001"

    ET.SubElement(physics, "max_step_size").text = "0.002"
    ET.SubElement(physics, "real_time_factor").text = "1"
    ET.SubElement(physics, "real_time_update_rate").text = "500"
    ET.SubElement(physics, "magnetic_field").text = "6e-06 2.3e-05 -4.2e-05"

    tree = ET.ElementTree(sdf)
    indent(sdf)

    tree.write(save_path, encoding="utf-8", xml_declaration=True)
