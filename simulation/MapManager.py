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

import pickle
from math import *
from random import *

import utils.geometrics_util as geometrics
from models.obstacles.OctagonObstacle import OctagonObstacle
from models.Pose import Pose
from models.Polygon import Polygon
from models.obstacles.RectangleObstacle import RectangleObstacle

seed(42)


class MapManager:

    def __init__(self, map_config):
        """
        Initializes a MapManager object
        :param map_config: The map configuration
        """
        self.current_obstacles = []
        self.current_goal = None
        self.cfg = map_config

    def random_map(self, world):
        """
        Generates a random map and goal
        :param world: The world the map is generated for
        """
        obstacles = []
        if self.cfg["obstacle"]["octagon"]["enabled"]:
            obstacles += self.__generate_octagon_obstacles(world)
        if self.cfg["obstacle"]["rectangle"]["enabled"]:
            obstacles += self.__generate_rectangle_obstacles(world)

        # update the current obstacles and goal
        self.current_obstacles = obstacles
        self.add_new_goal()

        # apply the new obstacles and goal to the world
        self.apply_to_world(world)

    def add_new_goal(self):
        """
        Adds a new goal
        """
        while True:
            goal = self.__generate_new_goal()
            intersects = self.__check_obstacle_intersections(goal)
            if not intersects:
                self.current_goal = goal
                break

    def __generate_octagon_obstacles(self, world):
        """
        Generate random octagon obstacles
        :param world: The world for which they are generated
        :return: List of generated octagon obstacles
        """
        obs_radius = self.cfg["obstacle"]["octagon"]["radius"]
        obs_min_count = self.cfg["obstacle"]["octagon"]["min_count"]
        obs_max_count = self.cfg["obstacle"]["octagon"]["max_count"]
        obs_min_dist = self.cfg["obstacle"]["octagon"]["min_distance"]
        obs_max_dist = self.cfg["obstacle"]["octagon"]["max_distance"]

        # generate the obstacles
        obstacles = []
        obs_dist_range = obs_max_dist - obs_min_dist
        num_obstacles = randrange(obs_min_count, obs_max_count + 1)

        test_geometries = [r.global_geometry for r in world.robots]
        while len(obstacles) < num_obstacles:

            # generate position
            dist = obs_min_dist + (random() * obs_dist_range)
            phi = -pi + (random() * 2 * pi)
            x = dist * sin(phi)
            y = dist * cos(phi)

            # generate orientation
            theta = -pi + (random() * 2 * pi)

            # test if the obstacle overlaps the robots or the goal
            obstacle = OctagonObstacle(obs_radius, Pose(x, y, theta))
            intersects = False
            for test_geometry in test_geometries:
                intersects |= geometrics.convex_polygon_intersect_test(test_geometry, obstacle.global_geometry)
            if not intersects:
                obstacles.append(obstacle)
        return obstacles

    def __generate_rectangle_obstacles(self, world):
        """
        Generate random rectangle obstacles
        :param world: The world for which they are generated
        :return: List of generated rectangle obstacles
        """
        obs_min_dim = self.cfg["obstacle"]["rectangle"]["min_dim"]
        obs_max_dim = self.cfg["obstacle"]["rectangle"]["max_dim"]
        obs_max_combined_dim = self.cfg["obstacle"]["rectangle"]["max_combined_dim"]
        obs_min_count = self.cfg["obstacle"]["rectangle"]["min_count"]
        obs_max_count = self.cfg["obstacle"]["rectangle"]["max_count"]
        obs_min_dist = self.cfg["obstacle"]["rectangle"]["min_distance"]
        obs_max_dist = self.cfg["obstacle"]["rectangle"]["max_distance"]

        # generate the obstacles
        obstacles = []
        obs_dim_range = obs_max_dim - obs_min_dim
        obs_dist_range = obs_max_dist - obs_min_dist
        num_obstacles = randrange(obs_min_count, obs_max_count + 1)

        test_geometries = [r.global_geometry for r in world.robots]
        while len(obstacles) < num_obstacles:
            # generate dimensions
            width = obs_min_dim + (random() * obs_dim_range )
            height = obs_min_dim + (random() * obs_dim_range )
            while width + height > obs_max_combined_dim:
                height = obs_min_dim + (random() * obs_dim_range )

            # generate position
            dist = obs_min_dist + (random() * obs_dist_range)
            phi = -pi + (random() * 2 * pi)
            x = dist * sin(phi)
            y = dist * cos(phi)

            # generate orientation
            theta = -pi + (random() * 2 * pi)

            # test if the obstacle overlaps the robots or the goal
            obstacle = RectangleObstacle(width, height, Pose(x, y, theta))
            intersects = False
            for test_geometry in test_geometries:
                intersects |= geometrics.convex_polygon_intersect_test(test_geometry, obstacle.global_geometry)
            if not intersects:
                obstacles.append(obstacle)
        return obstacles

    def __generate_new_goal(self):
        """
        Generate a new random goal
        :return: The generated goal
        """
        min_dist = self.cfg["goal"]["min_distance"]
        max_dist = self.cfg["goal"]["max_distance"]
        goal_dist_range = max_dist - min_dist
        dist = min_dist + (random() * goal_dist_range)
        phi = -pi + (random() * 2 * pi)
        x = dist * sin(phi)
        y = dist * cos(phi)
        goal = [x, y]
        return goal

    def __check_obstacle_intersections(self, goal):
        """
        Check for intersections between the goal and the obstacles
        :param goal: The goal posibition
        :return: Boolean value indicating if the goal is too close to an obstacle
        """
        # generate a proximity test geometry for the goal
        min_clearance = self.cfg["goal"]["min_clearance"]
        n = 6   # goal is n sided polygon
        goal_test_geometry = []
        for i in range(n):
            goal_test_geometry.append(
                [goal[0] + min_clearance * cos(i * 2 * pi / n),
                 goal[1] + min_clearance * sin(i * 2 * pi / n)])
        goal_test_geometry = Polygon(goal_test_geometry)
        intersects = False
        for obstacle in self.current_obstacles:
            intersects |= geometrics.convex_polygon_intersect_test(goal_test_geometry, obstacle.global_geometry)
        return intersects

    def save_map(self, filename):
        """
        Save the map, including obstacles and goal, as well as the current random state to enable reproducibility
        :param filename: The filename under which the map shall be stored
        """
        with open(filename, 'wb') as file:
            pickle.dump(self.current_obstacles, file)
            pickle.dump(self.current_goal, file)
            pickle.dump(getstate(), file)

    def load_map(self, filename):
        """
        Load a map from the file
        :param filename: Filename from which the map shall be loaded
        """
        with open(filename, 'rb') as file:
            self.current_obstacles = pickle.load(file)
            self.current_goal = pickle.load(file)
            try:
                setstate(pickle.load(file))
            except EOFError:
                print("No random state stored")

    def apply_to_world(self, world):
        """
        Apply the current obstacles and goal to the world
        :param world: The world that shall be updated
        """
        # add the current obstacles
        for obstacle in self.current_obstacles:
            world.add_obstacle(obstacle)

        # program the robot supervisors
        for robot in world.robots:
            robot.supervisor.goal = self.current_goal[:]
