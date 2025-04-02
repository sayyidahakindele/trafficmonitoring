from typing import List, Tuple


class TrafficSignal:
    def __init__(self, roads: List[List], cycle: List[Tuple],
                 slow_distance: float, slow_factor: float, stop_distance: float):
        self.roads: List[List] = roads
        # self.roads_indexes: Set[int] = set(road.index for road in chain.from_iterable(roads))
        self.cycle: List[Tuple[bool]] = cycle
        self.current_cycle_index = 0
        self.slow_distance: float = slow_distance
        self.slow_factor: float = slow_factor
        self.stop_distance: float = stop_distance
        self.prev_update_time: float = 0
        self.pedestrian_signal = "Don't Walk"
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)

    @property
    def current_cycle(self) -> Tuple:
        return self.cycle[self.current_cycle_index]

    def update(self):
        self.current_cycle_index = (self.current_cycle_index + 1) % len(self.cycle)
        self._update_pedestrian_signal()

    def _update_pedestrian_signal(self):
        
        """Update the pedestrian signal based on the current cycle."""
        # Example logic: Pedestrian signal is "Walk" when all vehicle signals are red
        current_cycle = self.cycle[self.current_cycle_index]
        if all(not state for state in current_cycle):  # All vehicle signals are red
            self.pedestrian_signal = "Walk"
        else:
            self.pedestrian_signal = "Don't Walk"

    def get_pedestrian_signal(self) -> str:
        """Return the current pedestrian signal state."""
        return self.pedestrian_signal
