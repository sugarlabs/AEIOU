# Copyright (C) 2009, Aleksey Lim
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


Gst.init(None)


def aplay(name):
    global player

    player.set_state(Gst.State.NULL)
    player.props.uri = 'file://' + name
    player.set_state(Gst.State.PLAYING)


def astop():
    global player, fakesink

    player.set_state(Gst.State.NULL)
    player = fakesink = None


def eos_cb(bus, message):
    player.set_state(Gst.State.NULL)


def error_cb(bus, message):
    err, debug = message.parse_error()
    print('%s %s' % (err, debug))
    player.set_state(Gst.State.NULL)


player = Gst.ElementFactory.make('playbin', 'playbin')
player.set_property(
    "video-sink",
    Gst.ElementFactory.make('fakesink', 'fakesink'))

player.get_bus().add_signal_watch()
player.get_bus().connect('message::eos', eos_cb)
player.get_bus().connect('message::error', error_cb)
