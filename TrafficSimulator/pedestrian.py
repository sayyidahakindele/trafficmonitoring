from typing import List, Dict, Optional
from numpy.random import randint
from TrafficSimulator.road import Road

class Pedestrian:
    def __init__(self, path: List[int]):
        if len(path) != 4:
            raise ValueError(f"Invalid path: {path}. Expected format: [start_x, start_y, end_x, end_y]")
        self.path: List[int] = path  # [start_x, start_y, end_x, end_y]
        self.x: float = path[0]  # Current x-coordinate
        self.y: float = path[1]  # Current y-coordinate
        self.destination_x: float = path[2]  # Destination x-coordinate
        self.destination_y: float = path[3]  # Destination y-coordinate
        self.is_crossing: bool = False  # Whether the pedestrian is currently crossing
        self.waiting_time: float = 0.0  # Time spent waiting to cross

    def update_state(self, can_cross: bool):
        """Update pedestrian state based on whether they can cross."""
        if can_cross:
            self.is_crossing = True
            self.waiting_time = 0
            self._move_towards_destination()
        else:
            self.is_crossing = False
            self.waiting_time += 1

    def _move_towards_destination(self):
        """Move the pedestrian towards their destination."""
        step_size = 0.1  # Adjust this value for speed
        dx = self.destination_x - self.x
        dy = self.destination_y - self.y
        distance = (dx**2 + dy**2)**0.5

        if distance > step_size:
            self.x += step_size * (dx / distance)
            self.y += step_size * (dy / distance)
        else:
            self.x = self.destination_x
            self.y = self.destination_y
            self.is_crossing = False  # Reached destination
    
    def _stop_at_crosswalk_edge(self):
        """Stop the pedestrian at the edge of the crosswalk."""
        crosswalk_start_x, crosswalk_start_y = self.path[0], self.path[1]
        dx = crosswalk_start_x - self.x
        dy = crosswalk_start_y - self.y
        distance = (dx**2 + dy**2)**0.5

        if distance > 0.1:  # Stop slightly before the crosswalk
            step_size = 0.1
            self.x += step_size * (dx / distance)
            self.y += step_size * (dy / distance)