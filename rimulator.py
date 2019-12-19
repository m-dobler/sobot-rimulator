#!/usr/bin/env python

# Sobot Rimulator - A Robot Programming Tool
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Email mccrea.engineering@gmail.com for questions, comments, or to report bugs.

import sys
import yaml
import gi
from gi.repository import GLib

from views.SlamView import SlamView

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

import gui.frame
import gui.viewer

from models.map_manager import *
from models.robot import *
from models.world import *

from views.world_view import *
from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0  # hertz
OBS_RADIUS = 0.04  # meters


class Simulator:

    def __init__(self, cfg):
        # create the GUI
        self.viewer = gui.viewer.Viewer(self)

        # create the map manager
        self.map_manager = MapManager(OBS_RADIUS)

        # timing control
        self.period = 1.0 / REFRESH_RATE  # seconds

        self.cfg = cfg

        # gtk simulation event source - for simulation control
        self.sim_event_source = GLib.idle_add(self.initialize_sim, True)  # we use this opportunity to initialize the sim

        # start gtk
        gtk.main()

    def initialize_sim(self, random=False):
        # reset the viewer
        self.viewer.control_panel_state_init()

        # create the simulation world
        self.world = World(self.period)

        # create the robot
        robot = Robot(self.cfg["robot"])
        # Assign supervisor to the robot
        robot.supervisor = Supervisor(RobotSupervisorInterface(robot), self.cfg["robot"], self.cfg["control"])
        self.world.add_robot(robot)

        # generate a random environment
        if random:
            self.map_manager.random_map(self.world)
        else:
            self.map_manager.apply_to_world(self.world)

        # create the world view
        self.world_view = WorldView(self.world, self.viewer)
        self.slam_view = SlamView(self.world.supervisors[0].slam, self.viewer, OBS_RADIUS, self.cfg["robot"])

        # render the initial world
        self.draw_world()

    def play_sim(self):
        GLib.source_remove(
            self.sim_event_source)  # this ensures multiple calls to play_sim do not speed up the simulator
        self._run_sim()
        self.viewer.control_panel_state_playing()

    def pause_sim(self):
        GLib.source_remove(self.sim_event_source)
        self.viewer.control_panel_state_paused()

    def step_sim_once(self):
        self.pause_sim()
        self._step_sim()

    def end_sim(self, alert_text=''):
        GLib.source_remove(self.sim_event_source)
        self.viewer.control_panel_state_finished(alert_text)

    def reset_sim(self):
        self.pause_sim()
        self.initialize_sim()

    def save_map(self, filename):
        self.map_manager.save_map(filename)

    def load_map(self, filename):
        self.map_manager.load_map(filename)
        self.reset_sim()

    def random_map(self):
        self.pause_sim()
        self.initialize_sim(random=True)

    def draw_world(self):
        self.viewer.new_frame()  # start a fresh frame
        self.world_view.draw_world_to_frame()  # draw the world onto the frame
        self.slam_view.draw_slam_to_frame()
        self.viewer.draw_frame()  # render the frame

    def _run_sim(self):
        self.sim_event_source = GLib.timeout_add(int(self.period * 1000), self._run_sim)
        self._step_sim()

    def _step_sim(self):
        # increment the simulation
        try:
            self.world.step()
        except CollisionException:
            self.end_sim('Collision!')
        except GoalReachedException:
            self.map_manager.add_new_goal()
            self.map_manager.apply_to_world(self.world)

        # draw the resulting world
        self.draw_world()


if __name__ == "__main__":
    filename = "config.yaml" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    Simulator(cfg)
