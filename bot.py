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


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = "Alpitronic"  # This is your team name

        self.course = [
            Checkpoint(latitude=46.51526380018685, longitude=-2.106954221077432, radius=1),
            Checkpoint(latitude=47.80314416647888, longitude=-5.052251381828896, radius=1),
            Checkpoint(latitude=59.47704024721139, longitude=-45.43535463804069, radius=1),
            Checkpoint(latitude=61.29777135363086, longitude=-50.50614648992773, radius=1),
            Checkpoint(latitude=74.01161191565813, longitude=-78.7927999147886, radius=1),
            Checkpoint(latitude=74.25173507721656, longitude=-96.65858010074633, radius=1),
            Checkpoint(latitude=73.72498541615348, longitude=-111.926159581506, radius=1),
            Checkpoint(latitude=74.40777471749568, longitude=-115.8822170582781, radius=1),
            Checkpoint(latitude=74.75897704017419, longitude=-120.1465931751061, radius=1),
            Checkpoint(latitude=75.04381102956535, longitude=-125.4345462396673, radius=1),
            Checkpoint(latitude=71.70547802179384, longitude=-127.951341529295, radius=1),
            Checkpoint(latitude=69.83455259335703, longitude=-137.1310063552145, radius=1),
            Checkpoint(latitude=70.73255432537843, longitude=-148.2239948674155, radius=1),
            Checkpoint(latitude=71.70038417142847, longitude=-157.2544217758774, radius=1),
            Checkpoint(latitude=69.35823694650743, longitude=-166.6847073961097, radius=1),
            Checkpoint(latitude=65.04357281610142, longitude=-169.891701898396, radius=1),
            Checkpoint(latitude=62.75645054920246, longitude=-167.6184920731297, radius=1),
            Checkpoint(latitude=48.69476863709392, longitude=-170.0381425172147, radius=1),
            Checkpoint(latitude=16.3091231357451, longitude=-178.6906302734677, radius=1),
            Checkpoint(latitude=3.793378485018821, longitude=120.0750675981632, radius=1),
            Checkpoint(latitude=-4.371808511810304, longitude=117.0937656707797, radius=1),
            Checkpoint(latitude=-4.629279687584559, longitude=114.4115097858007, radius=1),
            Checkpoint(latitude=-5.764862726763404, longitude=106.0386820822321, radius=1),
            Checkpoint(latitude=-6.11001139609985, longitude=105.7870113471664, radius=1),
            Checkpoint(latitude=-6.29742096732878, longitude=105.5319416909656, radius=1),
            Checkpoint(latitude=-6.114084860396257, longitude=104.6250388648793, radius=1),
            Checkpoint(latitude=-6.022524480367786, longitude=80.03577043127072, radius=1),
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

        current_position_terrain = world_map(latitudes=latitude, longitudes=longitude)
        # ===========================================================

        self.course = self.course

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
                break

        return instructions
