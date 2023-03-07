# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

bl_info = {
    "name": "SharpOcarina Export",
    "author": "dr.doodongo, Dragorn421, Campbell Barton, Bastien Montagne",
    "version": (1, 0, 3),
    "blender": (3, 0, 0),
    "location": "File > Export",
    "description": "Sharp Ocarina Tag Manager",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import os
import bpy

from pathlib import Path
from . import export
from . import properties
from . import interface

def reload_all_modules(log=True):
    global modules

    import importlib

    # the global variable "modules" is kept for the next reload
    if "modules" not in globals():
        if log:
            print('"modules" not in globals()')

        modules = dict()

    addon_dir = Path(__file__).parent

    if log:
        print("__file__ =", __file__)
        print("addon_dir =", addon_dir)

    for py_path in addon_dir.glob("**/*.py"):
        if py_path == Path(__file__):
            continue

        py_path = py_path.relative_to(addon_dir)
        if py_path.name == "__init__.py":
            n = "." + ".".join(py_path.parent.parts)
        else:
            n = "." + ".".join((*py_path.parent.parts, py_path.name.removesuffix(".py")))

        if n in modules:
            if log:
                print(f"importlib.reload(modules[n={n!r}])")

            importlib.reload(modules[n])
        else:
            if log:
                print(f"modules[n={n!r}] = importlib.import_module(n={n!r}, __package__={__package__!r})")

            modules[n] = importlib.import_module(n, __package__)


def register():
    reload_all_modules()
    Path(__file__).touch()

    export.register()
    properties.register()
    interface.register()

    print("OK!")


def unregister():
    export.unregister()
    properties.unregister()
    interface.unregister()

    Path(__file__).touch()


if __name__ == "__main__":
    register()