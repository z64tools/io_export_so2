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
    "name": "SOTM",
    "author": "Rankaisija, Campbell Barton, Bastien Montagne",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "File > Export",
    "description": "Sharp Ocarina Tag Manager",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import os
import bpy

from . import export
from . import properties
from . import interface


def register():
    print("Register Export")
    export.register()
    print("Register Properties")
    properties.register()
    print("Register Interface")
    interface.register()

    print("OK!")


def unregister():
    export.unregister()
    properties.unregister()
    interface.unregister()


if __name__ == "__main__":
    register()