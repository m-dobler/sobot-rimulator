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


import utils.linalg2_util as linalg

VECTOR_LEN = 0.75  # length of heading vector


class AvoidObstaclesControllerView:

    def __init__(self, supervisor):
        self.supervisor = supervisor
        self.avoid_obstacles_controller = supervisor.avoid_obstacles_controller

    # draw a representation of the avoid-obstacles controller's internal state to the frame
    def draw_avoid_obstacles_controller_to_frame(self, frame):
        robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()

        # draw the detected environment boundary (i.e. sensor readings)
        obstacle_vertexes = self.avoid_obstacles_controller.obstacle_vectors[:]
        obstacle_vertexes.append(obstacle_vertexes[0])  # close the drawn polygon
        obstacle_vertexes = linalg.rotate_and_translate_vectors(obstacle_vertexes, robot_theta, robot_pos)
        frame.add_lines([obstacle_vertexes],
                        linewidth=0.005,
                        color="black",
                        alpha=1.0)

        # draw the computed avoid-obstacles vector
        ao_heading_vector = linalg.scale(linalg.unit(self.avoid_obstacles_controller.ao_heading_vector), VECTOR_LEN)
        vector_line = [[0.0, 0.0], ao_heading_vector]
        vector_line = linalg.rotate_and_translate_vectors(vector_line, robot_theta, robot_pos)
        frame.add_lines([vector_line],
                        linewidth=0.02,
                        color="red",
                        alpha=1.0)
