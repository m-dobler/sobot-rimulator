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


class Frame:

    def __init__(self):
        """
        Initializes a Frame object with an empty list of objects to be drawn
        """
        self.draw_list = []

    def add_circle(self,
                   pos, radius,
                   color, alpha=None):
        """
        Adds a circle to the list of objects to be drawn
        :param pos: Position of the center of the circle
        :param radius: Radius of the circle
        :param color: Color of the circle
        :param alpha: Alpha value of the color of the circle
        """
        self.draw_list.append({
            'type': 'circle',
            'pos': pos,
            'radius': radius,
            'color': color,
            'alpha': alpha
        })

    def add_polygons(self,
                     polygons,
                     color, alpha=None):
        """
        Adds a polygon to the list of objects to be drawn
        :param polygons: List of polygon vertices
        :param color: Color of the polygon
        :param alpha: Alpha value of the color of the polygon
        """
        self.draw_list.append({
            'type': 'polygons',
            'polygons': polygons,
            'color': color,
            'alpha': alpha
        })

    def add_lines(self,
                  lines, linewidth,
                  color, alpha=None):
        """
        Adds lines to the list of objects to be drawn
        :param lines: The list of the vertices of the lines
        :param linewidth: The width of the lines
        :param color: Color of the lines
        :param alpha: Alpha value of the color of the lines
        """
        self.draw_list.append({
            'type': 'lines',
            'lines': lines,
            'linewidth': linewidth,
            'color': color,
            'alpha': alpha
        })

    def add_ellipse(self,
                    pos, angle,
                    radius_x, radius_y,
                    color, alpha=None):
        """
        Adds an ellipse to the list of objects to be drawn
        :param pos: Position of the center of the ellipse
        :param angle: Angle of the x side
        :param radius_x: "Radius" of one ellipse side
        :param radius_y: "Radius" of the other ellipse side, perpendicular to the radius_x
        :param color: Color of the ellipse
        :param alpha: Alpha value of the color of the ellipse
        """
        self.draw_list.append({
            'type': 'ellipse',
            'pos': pos,
            'angle': angle,
            'radius_x': radius_x,
            'radius_y': radius_y,
            'color': color,
            'alpha': alpha
        })
