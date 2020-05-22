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


from math import *

import utils.linalg2_util as linalg


class ProximitySensorPlotter:

    def __init__(self, proximity_sensor, cone_angle):
        """
        Initializes a ProximitySensorPlotter object
        :param proximity_sensor: The underlying proximity sensor
        :param cone_angle: The cone angle that should be used for plotting
        """
        self.proximity_sensor = proximity_sensor
        self.cone_angle = cone_angle

    def draw_proximity_sensor_to_frame(self, frame):
        """
        Draws the proximity sensor to a frame
        :param frame: The frame to be used
        """
        proximity_sensor = self.proximity_sensor

        # grab proximity sensor pose values
        sensor_pos, sensor_theta = proximity_sensor.pose.vunpack()

        # build the sensor cone
        r = proximity_sensor.max_range
        sensor_cone_poly = [[0.0, 0.0],
                            [r * cos(-self.cone_angle / 2), r * sin(-self.cone_angle / 2)],
                            [r, 0.0],
                            [r * cos(self.cone_angle / 2), r * sin(self.cone_angle / 2)]]
        sensor_cone_poly = linalg.rotate_and_translate_vectors(sensor_cone_poly,
                                                               sensor_theta,
                                                               sensor_pos)

        # shade the sensor cone according to positive detection
        if self.proximity_sensor.target_delta is not None:
            alpha = 0.9 - 0.8 * self.proximity_sensor.target_delta
        else:
            alpha = 0.1

        # add the sensor cone to the frame
        frame.add_polygons([sensor_cone_poly],
                           color="red",
                           alpha=alpha)

        # === FOR DEBUGGING: ===
        # self._draw_detector_line_to_frame()
        # self._draw_detector_line_origins_to_frame()
        # self._draw_bounding_circle_to_frame()
        # self._draw_detection_to_frame()

    def _draw_detection_to_frame(self, frame):
        """
        Visualize the detection of the proximity sensor
        :param frame: The frame to be used
        """
        target_delta = self.proximity_sensor.target_delta
        if target_delta is not None:
            detector_endpoints = self.proximity_sensor.detector_line.vertexes
            detector_vector = linalg.sub(detector_endpoints[1], detector_endpoints[0])
            target_vector = linalg.add(detector_endpoints[0], linalg.scale(detector_vector, target_delta))

            frame.add_circle(pos=target_vector,
                             radius=0.02,
                             color="black",
                             alpha=0.7)

    def _draw_detector_line_to_frame(self, frame):
        """
        Draws a detector line to a frame
        :param frame: The frame to be used
        """
        vertexes = self.proximity_sensor.detector_line.vertexes

        frame.add_lines([vertexes],
                        linewidth=0.005,
                        color="black",
                        alpha=0.7)

    def _draw_detector_line_origins_to_frame(self, frame):
        """
        Draw the detector line origins to a frame
        :param frame: The frame to be used
        """
        origin = self.proximity_sensor.detector_line.vertexes[0]
        frame.add_circle(pos=(origin[0], origin[1]),
                         radius=0.02,
                         color="black")

    def _draw_bounding_circle_to_frame(self, frame):
        """
        Draws a bounding circle fully containing the proximity snesor detector line to the frame
        :param frame: The frame to be used
        """
        c, r = self.proximity_sensor.detector_line.bounding_circle
        frame.add_circle(pos=c,
                         radius=r,
                         color="black",
                         alpha=0.2)
        frame.add_circle(pos=c,
                         radius=0.005,
                         color="black",
                         alpha=0.3)
