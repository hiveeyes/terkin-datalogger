# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import os
import sys
import logging
"""
==========
Motivation
==========

Tool to compile entire subdirectory to .mpy files [1].

Remark: The canonical implementation of this is `mpy_cross_all.py`_.
This program was started before being able to find it in time.

.. _mpy_cross_all.py: https://github.com/micropython/micropython/blob/master/tools/mpy_cross_all.py

Q: Isn't it just a 1-line shell command? E.g. something like 
   ``for file in $(find *.py); do mpy-cross $file; done``

A: Apparently not a one-line shell command, because it needs to pass 
   arguments down to mpy-cross, be able to compile .mpy in place or 
   in a dedicated (non existing) dir, then likely few more features 
   pop up. But it definitely going to be pretty simple (for starters) 
   Python script, and that point that we should standardize on it.

A: Makefile just calls that tool, instead of containing bunch of 
   glitchy shell magic.


=========
Rationale
=========
We found ``py_compile`` [2] but this isn't there yet.
On the other hand, we find [3] and [4] to be pretty interesting.
Nevertheless, we felt there's still a tooling gap so we built this.

After finally finding [5], [1] makes more sense to us.


============
More tooling
============
See also [10-12].


[1] https://github.com/micropython/micropython/issues/3040
[2] https://github.com/pfalcon/pycopy-lib/blob/master/py_compile/py_compile.py
[3] https://github.com/micropython/micropython/pull/4917
[4] https://github.com/micropython/micropython/pull/3034
[5] https://github.com/micropython/micropython/blob/master/tools/mpy_cross_all.py

[10] https://community.hiveeyes.org/t/micropython-tooling/2390
[11] https://community.hiveeyes.org/t/running-rshell-natively-on-windows/1774
[12] https://community.hiveeyes.org/t/ble-gatt-mit-nrf51822-oder-spbtle-rf-unter-micropython/2374/9
"""

# Setup logging.
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s [%(name)-10s] %(levelname)-7s: %(message)s')
log = logging.getLogger(__file__)
#log.setLevel(logging.DEBUG)


class DirectoryProcessingError(Exception):
    pass


def walk_directory(directory):
    for root, directories, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(root, filename)


def walk_pyfiles(directory):
    for filename in walk_directory(directory):
        if filename.endswith('.py'):
            yield filename


def compile_tree_inline(directory):
    import mpy_cross
    files_touched = []
    for py_file in walk_pyfiles(directory):
        log.info('Compiling "{}" using mpy-cross'.format(py_file))
        mpy_cross.run(py_file)
        mpy_file = py_file.replace('.py', '.mpy')
        files_touched.append(mpy_file)
    return files_touched


if __name__ == '__main__':
    directory = None
    try:
        directory = sys.argv[1]
        if not os.path.exists(directory):
            raise KeyError()
    except:
        log.error('"{}" is not a directory or does not exist. Please specify directory to compile.'.format(directory))
        sys.exit(2)

    # Compile a directory worth of .py files to .mpy files.
    compile_tree_inline(directory)
