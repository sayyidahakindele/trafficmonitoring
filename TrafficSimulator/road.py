from collections import deque
from typing import Deque, Optional, Tuple, List

from scipy.spatial import distance

from TrafficSimulator.traffic_signal import TrafficSignal
from TrafficSimulator.vehicle import Vehicle


class Road:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int], index: int):
        self.start = start
        self.end = end
        self.index = index

        self.vehicles: Deque[Vehicle] = deque()
        self.crosswalks: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        self.length: float = distance.euclidean(self.start, self.end)
        self.angle_sin: float = (self.end[1] - self.start[1]) / self.length
        self.angle_cos: float = (self.end[0] - self.start[0]) / self.length

        self.has_traffic_signal: bool = False
        self.traffic_signal: Optional[TrafficSignal] = None
        self.traffic_signal_group: Optional[int] = None

        self.horizontal_pedestrian_signal: Optional[TrafficSignal] = None
        self.vertical_pedestrian_signal: Optional[TrafficSignal] = None
        self.pedestrians_crossing: bool = False
        self.pedestrian_crossing_timer: float = 0.0

    def set_traffic_signal(self, signal: TrafficSignal, group: int):
        self.has_traffic_signal = True
        self.traffic_signal = signal
        self.traffic_signal_group = group

    def __str__(self):
        return f'Road {self.index}'

    @property
    def traffic_signal_state(self):
        """ Returns the traffic signal state if the road has a traffic signal, else True"""
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

    def set_pedestrian_signal(self, signal: TrafficSignal, direction: str):
        """Sets the pedestrian signal for a specific direction (horizontal/vertical)."""
        if direction == "horizontal":
            self.horizontal_pedestrian_signal = signal
        elif direction == "vertical":
            self.vertical_pedestrian_signal = signal    

    def add_crosswalk(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Adds a crosswalk to the road."""
        self.crosswalks.append((start, end))
        
    def update(self, dt, sim_t):
        n = len(self.vehicles)
        if n > 0:
            lead: Vehicle = self.vehicles[0]

            # Check for traffic signal
            if self.traffic_signal_state:
                # If traffic signal is green (or doesn't exist), let vehicles pass
                lead.unstop(sim_t)
                for vehicle in self.vehicles:
                    vehicle.unslow()
            elif self.has_traffic_signal:
                # The traffic signal is red (existence checked to access its stop_distance)
                lead_can_stop_safely = lead.x <= self.length - self.traffic_signal.stop_distance / 1.5
                # This check is to ensure that we don't stop vehicles that are too close to the traffic
                # signal when it turns to yellow. In such a case, the vehicle should pass as quickly as possible,
                # without being even slowed down
                if lead_can_stop_safely:
                    lead.slow(self.traffic_signal.slow_factor)  # slow vehicles in slow zone
                    lead_in_stop_zone = self.length - self.traffic_signal.stop_distance <= lead.x
                    if lead_in_stop_zone:
                        lead.stop(sim_t)

            if self.pedestrians_crossing:
                self.pedestrian_crossing_timer -= dt
                if self.pedestrian_crossing_timer <= 0:
                    self.pedestrians_crossing = False
            elif self.horizontal_pedestrian_signal and self.horizontal_pedestrian_signal.current_cycle[0]:
                self.pedestrians_crossing = True
                self.pedestrian_crossing_timer = self.length / 1.4  # Assuming pedestrian speed is 1.4 m/s
            elif self.vertical_pedestrian_signal and self.vertical_pedestrian_signal.current_cycle[0]:
                self.pedestrians_crossing = True
                self.pedestrian_crossing_timer = self.length / 1.4

            # Update first vehicle
            lead.update(None, dt, self)
            # Update other vehicles
            for i in range(1, n):
                lead = self.vehicles[i - 1]
                self.vehicles[i].update(lead, dt, self)
