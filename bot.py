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
        # This is the course that the ship has to follow
        self.course = [
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
        print(current_position_forecast, current_position_terrain)
        # ===========================================================

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
