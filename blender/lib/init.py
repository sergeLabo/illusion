# Copyright (C) Labomedia Mars 2012
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
#############################################################################

import GameLogic as gl

# ------------ Set list for get_osc ---------------- #
gl.connected = []
gl.socket = []

for i in range(len(gl.listen)):
    gl.connected.append(False)
    gl.socket.append(0)

# ------------ Set some var ---------------- #
gl.tempo = 0

# ------------ Set gl.attribution dict ---------------- #
gl.attribution = { "n0_text": 0 }


for key, value in gl.attribution.items():
    setattr(gl, key, value)
