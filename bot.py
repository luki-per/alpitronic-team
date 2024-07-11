# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401
from collections.abc import Callable

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    Vector,
    config,
)
from vendeeglobe.utils import distance_on_surface


def get_wind_angle(v1, v2):
    # Calculate dot product of v1 and v2
    dot_product = np.dot(v1, v2)

    # Calculate magnitudes of v1 and v2
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)

    # Calculate the cosine of the angle
    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)

    # Ensure the cosine value is within the valid range for arccos to avoid numerical errors
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    # Calculate the angle in radians
    angle_radians = np.arccos(cos_angle)

    # Convert the angle to degrees
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees


def get_course_rating(course, forecast):
    course_rating = 0

    # Iterate through the course list to calculate direction vectors
    for i in range(len(course) - 1):
        current_checkpoint = course[i]
        next_checkpoint = course[i + 1]

        # Calculate direction vector (delta_latitude, delta_longitude)
        delta_latitude = next_checkpoint.latitude - current_checkpoint.latitude
        delta_longitude = next_checkpoint.longitude - current_checkpoint.longitude

        ship_direction_vector = (delta_latitude, delta_longitude)
        wind_direction_vector = forecast(
            latitudes=current_checkpoint.latitude, longitudes=current_checkpoint.longitude, times=3
        )
        wind_angle = get_wind_angle(ship_direction_vector, wind_direction_vector)
        if 100 > wind_angle or wind_angle >= 250:
            course_rating += 1
    return course_rating


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = "TeamName"  # This is your team name
        # This is the course that the ship has to follow
        self.course = [
            Checkpoint(latitude=46.51526380018685, longitude=-2.106954221077432, radius=3),
            Checkpoint(latitude=47.80314416647888, longitude=-5.052251381828896, radius=10),
            Checkpoint(latitude=59.47704024721139, longitude=-45.43535463804069, radius=10),
            Checkpoint(latitude=61.29777135363086, longitude=-50.50614648992773, radius=10),
            Checkpoint(latitude=74.01161191565814, longitude=-78.7927999147886, radius=10),
            Checkpoint(latitude=74.25173507721657, longitude=-96.65858010074633, radius=10),
            Checkpoint(latitude=73.72498541615349, longitude=-111.926159581506, radius=10),
            Checkpoint(latitude=74.40777471749568, longitude=-115.8822170582781, radius=10),
            Checkpoint(latitude=74.75897704017419, longitude=-120.1465931751061, radius=10),
            Checkpoint(latitude=75.04381102956535, longitude=-125.4345462396673, radius=10),
            Checkpoint(latitude=71.40547802179384, longitude=-127.951341529295, radius=10),
            Checkpoint(latitude=69.83455259335703, longitude=-137.1310063552145, radius=10),
            Checkpoint(latitude=70.73255432537843, longitude=-148.2239948674155, radius=1),
            Checkpoint(latitude=71.70038417142847, longitude=-157.2544217758774, radius=1),
            Checkpoint(latitude=69.35823694650743, longitude=-166.6847073961097, radius=1),
            Checkpoint(latitude=65.04357281610142, longitude=-169.891701898396, radius=1),
            Checkpoint(latitude=62.75645054920246, longitude=-167.6184920731297, radius=1),
            Checkpoint(latitude=48.69476863709392, longitude=-170.0381425172147, radius=1),
            Checkpoint(latitude=19.22145017743467, longitude=-178.8238574058236, radius=1),
            Checkpoint(latitude=2.783378485018821, longitude=120.2750675981632, radius=1),
            Checkpoint(latitude=-4.371808511810304, longitude=116.3937656707797, radius=1),
            Checkpoint(latitude=-4.629279687584559, longitude=114.4115097858007, radius=1),
            Checkpoint(latitude=-5.764862726763404, longitude=106.0386820822321, radius=1),
            Checkpoint(latitude=-6.11001139609985, longitude=105.7870113471664, radius=1),
            Checkpoint(latitude=-6.29742096732878, longitude=105.5319416909656, radius=1),
            Checkpoint(latitude=-6.114084860396257, longitude=104.6250388648793, radius=1),
            Checkpoint(latitude=-4.80837396250466, longitude=80.12838504403044, radius=1),
            Checkpoint(latitude=12.32364950720728, longitude=51.06186749020405, radius=1),
            Checkpoint(latitude=11.68438658686913, longitude=43.91390326465574, radius=1),
            Checkpoint(latitude=29.07795456671188, longitude=32.82494554815788, radius=1),
            Checkpoint(latitude=29.89992425488417, longitude=32.62119154396041, radius=1),
            Checkpoint(latitude=31.71593248722569, longitude=32.48269069721169, radius=1),
            Checkpoint(latitude=36.95342443068156, longitude=12.50156611166445, radius=1),
            Checkpoint(latitude=37.78784203471952, longitude=9.74117685531434, radius=1),
            Checkpoint(latitude=35.75316212323058, longitude=-6.65594857105228, radius=1),
            Checkpoint(latitude=37.07851166092445, longitude=-9.881346233229701, radius=1),
            Checkpoint(latitude=43.41671723878878, longitude=-9.59315063982473, radius=1),
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=1,
            ),
        ]

        self.course_north = [
            Checkpoint(latitude=46.51526380018685, longitude=-2.106954221077432, radius=3),
            Checkpoint(latitude=47.80314416647888, longitude=-5.052251381828896, radius=10),
            Checkpoint(latitude=59.47704024721139, longitude=-45.43535463804069, radius=10),
            Checkpoint(latitude=61.29777135363086, longitude=-50.50614648992773, radius=10),
            Checkpoint(latitude=74.01161191565813, longitude=-78.7927999147886, radius=10),
            Checkpoint(latitude=74.25173507721656, longitude=-96.65858010074633, radius=10),
            Checkpoint(latitude=73.72498541615348, longitude=-111.926159581506, radius=10),
            Checkpoint(latitude=74.40777471749568, longitude=-115.8822170582781, radius=10),
            Checkpoint(latitude=74.75897704017419, longitude=-120.1465931751061, radius=10),
            Checkpoint(latitude=75.04381102956535, longitude=-125.4345462396673, radius=10),
            Checkpoint(latitude=71.40547802179384, longitude=-127.951341529295, radius=10),
            Checkpoint(latitude=69.83455259335703, longitude=-137.1310063552145, radius=10),
            Checkpoint(latitude=70.73255432537843, longitude=-148.2239948674155, radius=10),
            Checkpoint(latitude=71.70038417142847, longitude=-157.2544217758774, radius=10),
            Checkpoint(latitude=69.35823694650743, longitude=-166.6847073961097, radius=10),
            Checkpoint(latitude=65.04357281610142, longitude=-169.891701898396, radius=10),
            Checkpoint(latitude=62.75645054920246, longitude=-167.6184920731297, radius=10),
            Checkpoint(latitude=48.69476863709392, longitude=-170.0381425172147, radius=10),
            Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1990.0),
        ]

        self.course_panama = [
            Checkpoint(latitude=46.47535337182985, longitude=-1.987242046570165, radius=1),
            Checkpoint(latitude=17.75395401995559, longitude=-68.53393421733739, radius=1),
            Checkpoint(latitude=9.596699224197881, longitude=-80.10762674052567, radius=1),
            Checkpoint(latitude=7.995870801960294, longitude=-79.22779328612677, radius=1),
            Checkpoint(latitude=6.481266459594321, longitude=-80.24932074214756, radius=1),
            Checkpoint(latitude=20.2091231357451, longitude=-160.6906302734677, radius=1),
        ]

        self.course_australia = [
            Checkpoint(latitude=-22.3682399229219, longitude=169.7716302925487, radius=1),
            Checkpoint(latitude=-38.89756012433131, longitude=148.6584464632712, radius=1),
            Checkpoint(latitude=-39.43712291429078, longitude=146.9397239577109, radius=1),
            Checkpoint(latitude=-39.71964415915588, longitude=146.6436592429874, radius=1),
            Checkpoint(latitude=-38.11473889710815, longitude=139.7076193078962, radius=1),
            Checkpoint(latitude=-34.96547393476094, longitude=114.7356930791068, radius=1),
        ]



    def run(
            self,
            t: float,
            dt: float,
            longitude: float,
            latitude: float,
            heading: float,
            speed: float,
            vector: np.ndarray,
            forecast: Callable,
            world_map: Callable,
    ) -> Instructions:
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            Method to query the weather forecast for the next 5 days.
            Example:
            current_position_forecast = forecast(
                latitudes=latitude, longitudes=longitude, times=0
            )
        world_map:
            Method to query map of the world: 1 for sea, 0 for land.
            Example:
            current_position_terrain = world_map(
                latitudes=latitude, longitudes=longitude
            )

        Returns
        -------
        instructions:
            A set of instructions for the ship. This can be:
            - a Location to go to
            - a Heading to point to
            - a Vector to follow
            - a number of degrees to turn Left
            - a number of degrees to turn Right

            Optionally, a sail value between 0 and 1 can be set.
        """
        # Initialize the instructions
        instructions = Instructions()

        # TODO: Remove this, it's only for testing =================
        current_position_forecast = forecast(
            latitudes=latitude, longitudes=longitude, times=0
        )
        current_position_terrain = world_map(latitudes=latitude, longitudes=longitude)
        # ===========================================================

        # Get the course rating
        course_rating_north = get_course_rating(self.course_north, forecast)
        course_rating_panama = get_course_rating(self.course_panama, forecast)

        print(course_rating_north)
        print(course_rating_panama)

        # Go through all checkpoints and find the next one to reach
        for ch in self.course:
            # Compute the distance to the checkpoint
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            instructions.sail = 1.0
            # Check if the checkpoint has been reached
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                # instructions.vector = Vector(
                #    u=current_position_forecast[0], v=current_position_forecast[1]
                # )
                wind_angle = get_wind_angle(vector, current_position_forecast)
                # print(wind_angle)
                break

        return instructions
