from typing import List, Dict, Optional

from numpy.random import randint

from TrafficSimulator.road import Road
from TrafficSimulator.vehicle import Vehicle


class VehicleGenerator:
    def __init__(self, vehicle_rate: int, paths: List[List], inbound_roads: Dict[int, Road]):
        self._vehicle_rate: int = vehicle_rate
        self._paths: List[List] = paths
        self._prev_gen_time: float = 0

        # Storing the list of the first roads of the vehicle paths. Used in the update() function
        # upon vehicle generation to check if there's sufficient space in the road to add a vehicle
        self._inbound_roads: Dict[int, Road] = inbound_roads

    def _generate_vehicle(self) -> Vehicle:
        """Returns a random vehicle from self.vehicles with random proportions"""
        total = sum(weight for weight, path in self._paths)
        r = randint(0, total)
        for (weight, path) in self._paths:
            r -= weight
            if r <= 0:
                return Vehicle(path)

    def update(self, curr_t: float, n_vehicles_generated: int) -> Optional[int]:
        """Generates a vehicle if the generation conditions are satisfied
        :return: road index if a vehicle was generated, else None
        """
        # If there's no vehicles on the map, or if the time elapsed after last
        # generation is greater than the vehicle rate, generate a vehicle
        time_elapsed = curr_t - self._prev_gen_time >= 60 / self._vehicle_rate
        if not n_vehicles_generated or time_elapsed:
            vehicle: Vehicle = self._generate_vehicle()
            road: Road = self._inbound_roads[vehicle.path[0]]
            # If the road is empty, or there's sufficient space for the generated vehicle, add it
            if not road.vehicles or road.vehicles[-1].x > vehicle.s0 + vehicle.length:
                vehicle.index = n_vehicles_generated
                road.vehicles.append(vehicle)
                self._prev_gen_time = curr_t
                return road.index
        return None
