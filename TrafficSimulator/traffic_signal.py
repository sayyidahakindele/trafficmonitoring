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
        self.can_cross_horizontal: bool = False
        self.can_cross_vertical: bool = False
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)

    @property
    def current_cycle(self) -> Tuple:
        return self.cycle[self.current_cycle_index]

    def update(self):
        self.current_cycle_index = (self.current_cycle_index + 1) % len(self.cycle)
        self._update_pedestrian_signal()
        print(f"New Cycle Index = {self.current_cycle_index}, "
          f"Current Cycle = {self.cycle[self.current_cycle_index]}\n")

    def _update_pedestrian_signal(self):
        """Update the pedestrian signals based on the current cycle."""
        current_cycle = self.cycle[self.current_cycle_index]

        # Assign pedestrian signals based on the current cycle
        self.can_cross_horizontal = current_cycle[1]  # Horizontal pedestrians can cross when vertical vehicles are moving
        self.can_cross_vertical = current_cycle[0]  # Vertical pedestrians can cross when horizontal vehicles are moving

        print(f"Updated Pedestrian Signals: Horizontal = {self.can_cross_horizontal}, Vertical = {self.can_cross_vertical}")

    def get_pedestrian_signal(self) -> Tuple[bool, bool]:
        """Return the current pedestrian signal states."""
        return self.can_cross_horizontal, self.can_cross_vertical
