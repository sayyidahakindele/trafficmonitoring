from trafficSimulator import Simulation
from trafficSimulator.curve import *

#
n = 15  # Curve resolution
a = 2  # Short offset from (0, 0)
b = 12  # Long offset from (0, 0)
length = 50  # Road length

# Nodes
WEST_RIGHT_START = (-b - length, a)
WEST_LEFT_START = (-b - length, -a)

SOUTH_RIGHT_START = (a, b + length)
SOUTH_LEFT_START = (-a, b + length)

EAST_RIGHT_START = (b + length, -a)
EAST_LEFT_START = (b + length, a)

NORTH_RIGHT_START = (-a, -b - length)
NORTH_LEFT_START = (a, -b - length)

WEST_RIGHT = (-b, a)
WEST_LEFT = (-b, -a)

SOUTH_RIGHT = (a, b)
SOUTH_LEFT = (-a, b)

EAST_RIGHT = (b, -a)
EAST_LEFT = (b, a)

NORTH_RIGHT = (-a, -b)
NORTH_LEFT = (a, -b)

# Roads
WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)

WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

WEST_STRAIGHT = (WEST_RIGHT, EAST_LEFT)
SOUTH_STRAIGHT = (SOUTH_RIGHT, NORTH_LEFT)
EAST_STRAIGHT = (EAST_RIGHT, WEST_LEFT)
NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)

WEST_RIGHT_TURN = turn_road(WEST_RIGHT, SOUTH_LEFT, TURN_RIGHT, n)
WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)

SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT, EAST_LEFT, TURN_RIGHT, n)
SOUTH_LEFT_TURN = turn_road(SOUTH_RIGHT, WEST_LEFT, TURN_LEFT, n)

EAST_RIGHT_TURN = turn_road(EAST_RIGHT, NORTH_LEFT, TURN_RIGHT, n)
EAST_LEFT_TURN = turn_road(EAST_RIGHT, SOUTH_LEFT, TURN_LEFT, n)

NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT, WEST_LEFT, TURN_RIGHT, n)
NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, EAST_LEFT, TURN_LEFT, n)

ROADS = [
    WEST_INBOUND,
    SOUTH_INBOUND,
    EAST_INBOUND,
    NORTH_INBOUND,

    WEST_OUTBOUND,
    SOUTH_OUTBOUND,
    EAST_OUTBOUND,
    NORTH_OUTBOUND,

    WEST_STRAIGHT,
    SOUTH_STRAIGHT,
    EAST_STRAIGHT,
    NORTH_STRAIGHT,

    *WEST_RIGHT_TURN,
    *WEST_LEFT_TURN,

    *SOUTH_RIGHT_TURN,
    *SOUTH_LEFT_TURN,

    *EAST_RIGHT_TURN,
    *EAST_LEFT_TURN,

    *NORTH_RIGHT_TURN,
    *NORTH_LEFT_TURN
]


def turn(t): return range(t, t + n)


# Vehicle generator
VEHICLE_RATE = 30
EMS_VEHICLE_RATE = 4
PATHS = [
    [3, [0, 8, 6]],
    [1, [0, *turn(12), 5]],
    [1, [0, *turn(12 + n), 7]],

    [3, [1, 9, 7]],
    [1, [1, *turn(12 + 2 * n), 6]],
    [1, [1, *turn(12 + 3 * n), 4]],

    [3, [2, 10, 4]],
    [1, [2, *turn(12 + 4 * n), 7]],
    [1, [2, *turn(12 + 5 * n), 5]],

    [3, [3, 11, 5]],
    [1, [3, *turn(12 + 6 * n), 4]],
    [1, [3, *turn(12 + 7 * n), 6]]
]


def short_turn(t): return range(t + 2, t + n - 2)


# Intersections
t12 = short_turn(12)
t27 = short_turn(27)
t42 = short_turn(42)
t57 = short_turn(56)
t72 = short_turn(72)
t87 = short_turn(87)
t102 = short_turn(102)
t117 = short_turn(117)
d1 = {8: [9, 11, *t42, *t57, *t87, *t117]}
d2 = {9: [10, *t12, *t27, *t72, *t87, *t117]}
d3 = {10: [11, *t27, *t57, *t102, *t117]}
d4 = {11: [*t12, *t27, *t57, *t87]}
d5 = {road: [*t87] for road in t12}
d6 = {road: [*t57, *t72, *t117] for road in t27}
d7 = {road: [*t117] for road in t42}
d8 = {road: [*t87, *t102] for road in t57}
d9 = {road: [*t117] for road in t87}

INTERSECTIONS_DICT = {
    **d1,
    **d2,
    **d3,
    **d4,
    **d5,
    **d6,
    **d7,
    **d8,
    **d9
}

# Signals
SIGNALS = [[0, 2], [1, 3]]
CYCLE = [(False, True), (True, False)]
SLOW_DISTANCE = 50
SLOW_FACTOR = 0.4
STOP_DISTANCE = 15


def two_way_intersection():
    sim = Simulation()
    sim.create_roads(ROADS)
    sim.create_gen(VEHICLE_RATE, PATHS)
    sim.create_gen(EMS_VEHICLE_RATE, PATHS, ems=True)
    sim.create_signal(SIGNALS, CYCLE, SLOW_DISTANCE, SLOW_FACTOR, STOP_DISTANCE)
    sim.create_intersections(INTERSECTIONS_DICT)
    return sim

# nd[14] = [*t87]
# nd[15] = [*t87]
# nd[16] = [*t87]
# nd[17] = [*t87]
# nd[18] = [*t87]
# nd[19] = [*t87]
# nd[20] = [*t87]
# nd[21] = [*t87]
# nd[22] = [*t87]
# nd[23] = [*t87]
# nd[24] = [*t87]
# nd[29] = [*t56, *t72, *t117]
# nd[30] = [*t56, *t72, *t117]
# nd[31] = [*t56, *t72, *t117]
# nd[32] = [*t56, *t72, *t117]
# nd[33] = [*t56, *t72, *t117]
# nd[34] = [*t56, *t72, *t117]
# nd[35] = [*t56, *t72, *t117]
# nd[36] = [*t56, *t72, *t117]
# nd[37] = [*t56, *t72, *t117]
# nd[38] = [*t56, *t72, *t117]
# nd[39] = [*t56, *t72, *t117]
# nd[44] = [*t117]
# nd[45] = [*t117]
# nd[46] = [*t117]
# nd[47] = [*t117]
# nd[48] = [*t117]
# nd[49] = [*t117]
# nd[50] = [*t117]
# nd[51] = [*t117]
# nd[52] = [*t117]
# nd[53] = [*t117]
# nd[54] = [*t117]
# nd[59] = [*t87, *t102]
# nd[60] = [*t87, *t102]
# nd[61] = [*t87, *t102]
# nd[62] = [*t87, *t102]
# nd[63] = [*t87, *t102]
# nd[64] = [*t87, *t102]
# nd[65] = [*t87, *t102]
# nd[66] = [*t87, *t102]
# nd[67] = [*t87, *t102]
# nd[68] = [*t87, *t102]
# nd[69] = [*t87, *t102]
# nd[89] = [*t117]
# nd[90] = [*t117]
# nd[91] = [*t117]
# nd[92] = [*t117]
# nd[93] = [*t117]
# nd[94] = [*t117]
# nd[95] = [*t117]
# nd[96] = [*t117]
# nd[97] = [*t117]
# nd[98] = [*t117]
# nd[99] = [*t117]


# # n=15
# def short_turn(t): return range(t + 2, t + n - 2)


# NORTH_STRAIGHT_INTERSECTIONS = {
#     11: [10, 8, *t56, t12, *t27, *t87]}
# EAST_STRAIGHT_INTERSECTIONS = {10: [
#     9, 11, *t102, *t56, *t27, *t117]}
# SOUTH_STRAIGHT_INTERSECTIONS = {
#     9: [10, 8, *t87, *t72, *t27, t12]}
# WEST_STRAIGHT_INTERSECTIONS = {
#     8: [9, 11, *t87, *t56, *t42, *t117]}

# NORTH_RIGHT_TURN_INTERSECTIONS = {
#     road: [10, *t56] for road in t102}
# EAST_RIGHT_TURN_INTERSECTIONS = {
#     road: [9, *t27] for road in t72}
# SOUTH_RIGHT_TURN_INTERSECTIONS = {
#     road: [8, *t117] for road in t42}
# WEST_RIGHT_TURN_INTERSECTIONS = {
#     road: [11, *t87] for road in short_turn(12)}

# NORTH_LEFT_TURN_INTERSECTIONS = {road: [10, 8, *t42, *t87, *t27] for road in
#                                  t117}
# EAST_LEFT_TURN_INTERSECTIONS = {road: [11, 9, *t56, *t117, t12] for road in
#                                 t87}
# SOUTH_LEFT_TURN_INTERSECTIONS = {road: [10, 8, *t87, *t27, *t102] for road in
#                                  t56}
# WEST_LEFT_TURN_INTERSECTIONS = {road: [11, 9, *t56, *t117, *t72] for road in
#                                 t27}


# nd = {
#     **NORTH_STRAIGHT_INTERSECTIONS,
#     **EAST_STRAIGHT_INTERSECTIONS,
#     **SOUTH_STRAIGHT_INTERSECTIONS,
#     **WEST_STRAIGHT_INTERSECTIONS,

#     **NORTH_RIGHT_TURN_INTERSECTIONS,
#     **EAST_RIGHT_TURN_INTERSECTIONS,
#     **SOUTH_RIGHT_TURN_INTERSECTIONS,
#     **WEST_RIGHT_TURN_INTERSECTIONS,

#     **NORTH_LEFT_TURN_INTERSECTIONS,
#     **EAST_LEFT_TURN_INTERSECTIONS,
#     **SOUTH_LEFT_TURN_INTERSECTIONS,
#     **WEST_LEFT_TURN_INTERSECTIONS,
# }

# # i = 0
# # for k, v in nd.items():
# #     i += len(v)
# #     # print(k, v)
# # print(i)

# # print(sum(len(value for value in nd.values())))

# for key in range(300):
#     if key in nd:
#         value = sorted(nd[key], reverse=True)
#         if value:
#             for n in value:
#                 if n in nd and key in nd[n]:
#                     nd[n].remove(key)

# # for key in range(300):
# #     if key in nd:
# #         value = sorted(nd[key], reverse=True)
# #         if value:
# #             for n in value:
# #                 if n in nd and key in nd[n]:
# #                     nd[n].remove(key)

# # i = 0
# # for k, v in nd.items():
# #     i += len(v)
# #     # print(k, v)
# # print(i)

# # # print(sum[len(v for v in nd.values()]))

# for key in range(300):
#     if key in nd:
#         value = sorted(nd[key])
#         if value:
#             if len(value) > 11:
#                 print(f"nd[{key}] = {value}")
#                 # print(value)
#                 # chunks = [value[x:x+11] for x in range(0, len(value), 100)]
#                 # print(chunks)
#             else:
#                 print(f"nd[{key}] = *short_turn({value[0]-2})")

#             # print(key, value)
#             # for n in value:
#             #     if n in nd and key in nd[n]:
#             #         nd[n].remove(key)
