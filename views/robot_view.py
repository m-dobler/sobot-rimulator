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


from views.proximity_sensor_view import *
from views.supervisor_view import *


class RobotView:

    def __init__(self, robot):
        self.robot = robot
        self.robot_shape = robot.robot_cfg["top_plate"]

        # add the supervisor views for this robot
        self.supervisor_view = SupervisorView(robot.supervisor, robot.geometry)

        # add the IR sensor views for this robot
        self.ir_sensor_views = []
        for ir_sensor in robot.ir_sensors:
            self.ir_sensor_views.append(ProximitySensorView(ir_sensor))

        self.traverse_path = []  # this robot's traverse path

    def draw_robot_to_frame(self, frame, draw_invisibles=False):
        # update the robot traverse path
        position = self.robot.pose.vposition()
        self.traverse_path.append(position)

        # draw the internal state ( supervisor ) to the frame
        self.supervisor_view.draw_supervisor_to_frame(frame, draw_invisibles)

        # draw the IR sensors to the frame if indicated
        if draw_invisibles:
            for ir_sensor_view in self.ir_sensor_views:
                ir_sensor_view.draw_proximity_sensor_to_frame(frame)

        # draw the robot
        robot_bottom = self.robot.global_geometry.vertexes
        frame.add_polygons([robot_bottom],
                           color="blue",
                           alpha=0.5)
        # add decoration
        robot_pos, robot_theta = self.robot.pose.vunpack()
        robot_top = linalg.rotate_and_translate_vectors(self.robot_shape, robot_theta, robot_pos)
        frame.add_polygons([robot_top],
                           color="black",
                           alpha=0.5)

        # draw the robot's traverse path if indicated
        if draw_invisibles:
            self._draw_real_traverse_path_to_frame(frame)

    def _draw_real_traverse_path_to_frame(self, frame):
        frame.add_lines([self.traverse_path],
                        color="black",
                        linewidth=0.01)

    # draws the traverse path as dots weighted according to robot speed
    def _draw_rich_traverse_path_to_frame(self, frame):
        # when robot is moving fast, draw small, opaque dots
        # when robot is moving slow, draw large, transparent dots
        d_min, d_max = 0.0, 0.01574  # possible distances between dots
        r_min, r_max = 0.007, 0.02  # dot radius
        a_min, a_max = 0.3, 0.55  # dot alpha value
        m_r = (r_max - r_min) / (d_min - d_max)
        b_r = r_max - m_r * d_min
        m_a = (a_max - a_min) / (r_min - r_max)
        b_a = a_max - m_a * r_min

        prev_posn = self.traverse_path[0]
        for posn in self.traverse_path[1::1]:
            d = linalg.distance(posn, prev_posn)
            r = (m_r * d) + b_r
            a = (m_a * r) + b_a
            frame.add_circle(pos=posn,
                             radius=r,
                             color="black",
                             alpha=a)

            prev_posn = posn
