from typing import List, Dict, Optional
import numpy as np
from TrafficSimulator.road import Road
from TrafficSimulator.pedestrian import Pedestrian

class PedestrianGenerator:
    def __init__(self, pedestrian_rate: int, paths: List[List]):
        self._pedestrian_rate = pedestrian_rate
        self._paths = paths  # List of crosswalk paths
        self._crossing_requests: List[Pedestrian] = []  # Pedestrians waiting to cross

    def _generate_pedestrian(self) -> Pedestrian:
        """Generate a pedestrian with a random path."""
        path = self._paths[np.random.randint(len(self._paths))]
        # Offset the starting position slightly outside the crosswalk
        start_x, start_y, end_x, end_y = path
        offset = 10  # Adjust this value for how far outside the crosswalk pedestrians start
        if start_x == end_x:  # Vertical crosswalk
            start_y -= offset if start_y > end_y else -offset
        else:  # Horizontal crosswalk
            start_x -= offset if start_x > end_x else -offset
        return Pedestrian([start_x, start_y, end_x, end_y])

    def update(self, curr_t: float, can_cross: bool):
        """Generate pedestrians and process crossing requests."""
        for pedestrian in self._crossing_requests[:]:
            pedestrian.update_state(can_cross)
            if not pedestrian.is_crossing and (pedestrian.x == pedestrian.destination_x and pedestrian.y == pedestrian.destination_y):
                self._crossing_requests.remove(pedestrian)

        # Generate new pedestrians based on rate
        if np.random.random() < self._pedestrian_rate / 60:
            pedestrian = self._generate_pedestrian()
            self._crossing_requests.append(pedestrian)