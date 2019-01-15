#!/usr/bin/python

from __future__ import print_function, unicode_literals

import sys
import json
import numpy as np

inpfn, outfn = sys.argv[1:]

with open(inpfn, 'r') as f:
  world = json.load(f)

gate_width, gate_height = world['gate_size']
gate_wall_height = 2.0
gate_wall_width = 0.1

def yaw_matrix(angle):
  return np.array([[ np.cos(angle), -np.sin(angle), 0.0],
                  [  np.sin(angle),  np.cos(angle), 0.0],
                  [            0.0,            0.0, 1.0]])

def walls_for_gate(gate):
  R = yaw_matrix(gate['heading']/180.0*np.pi).T.dot
  gx, gy, _ = gate['position']

  # Right
  yield {"plane": {
           "start": np.r_[gx, gy, 0.0] + R([-gate_width/2.0 - gate_wall_width, 0.0,         0.0]),
           "stop":  np.r_[gx, gy, 0.0] + R([-gate_width/2.0                  , 0.0, gate_height])
         },
         "gate": gate['id']}

  # Left
  yield {"plane": {
           "start": np.r_[gx, gy, 0.0] + R([+gate_width/2.0                  , 0.0,         0.0]),
           "stop":  np.r_[gx, gy, 0.0] + R([+gate_width/2.0 + gate_wall_width, 0.0, gate_height])
         },
         "gate": gate['id']}

  # Top
  yield {"plane": {
           "start": np.r_[gx, gy, 0.0] + R([-gate_width/2.0 - gate_wall_width, 0.0, gate_height]),
           "stop":  np.r_[gx, gy, 0.0] + R([+gate_width/2.0 + gate_wall_width, 0.0, gate_wall_height])
         },
         "gate": gate['id']}
  

gate_ids_with_walls = set(w['gate'] for w in world['walls'] if 'gate' in w)

for gate in world['gates']:
  if gate['id'] in gate_ids_with_walls:
    print('Gate', gate['id'], 'already has walls; none generated.')
  else:
    print('Gate', gate['id'])
    world['walls'].extend(walls_for_gate(gate))

with open(outfn, 'w') as f:
  json.dump(world, f, default=list, indent=2)
