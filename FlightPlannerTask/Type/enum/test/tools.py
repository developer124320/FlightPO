# -*- coding: utf-8 -*-

# test/tools.py
# Part of ‘enum’, a package providing enumerated types for Python.
#
# Copyright © 2007–2015 Ben Finney <ben+python@benfinney.id.au>
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.

""" Helper tools for unit tests.
    """

import os.path
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.dirname(test_dir)
if not test_dir in sys.path:
    sys.path.insert(1, test_dir)
if not code_dir in sys.path:
    sys.path.insert(1, code_dir)


# Local variables:
# mode: python
# End:
# vim: filetype=python fileencoding=utf-8 :
