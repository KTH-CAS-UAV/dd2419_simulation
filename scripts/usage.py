#!/usr/bin/env python

"""
    @author: Daniel Duberg (dduberg@kth.se)
"""

from __future__ import print_function, unicode_literals
import os
import re


def how_to_use(usage, dir, file_type):
    file_type_length = len(file_type)
    print('')
    print(usage)
    print('')
    print('Where FILENAME is one of:')
    for file in sorted(os.listdir(dir)):
        if len(file) > file_type_length and file[-file_type_length:] == file_type:
            print("    * ", re.sub(re.escape(file_type) + '$', '', file))
