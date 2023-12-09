import math
import numpy as np

class SubwayStation:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.lines = []
        self.latitude = latitude
        self.longitude = longitude
        self.grid_point = self.calculate_grid_point()

    def __str__(self):
        return self.name
        
    # Convert geographical coordinates to grid points (haversine formula)

    def calculate_grid_point(self):
        R = 6371  # Earth radius in kilometers
        lat_rad = math.radians(self.latitude)
        lon_rad = math.radians(self.longitude)
        
        x = R * math.cos(lat_rad) * math.cos(lon_rad)
        y = R * math.cos(lat_rad) * math.sin(lon_rad)

        return x, y
    
class SubwayLine:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
# Subway stations
coney_island = SubwayStation("Coney Island Station", 40.5763, -73.9755)
j_st_metro_tech = SubwayStation("Jay Street Metro Tech Station", 40.6925, -73.9874)
w_4_st_wash_sq = SubwayStation("West 4th Street Washington Square", 40.7326, -74.0002)
one_four_5 = SubwayStation("145th Street", 40.8257, -73.9442)
herald_sq = SubwayStation("34th Street Herald Square", 40.7495, -73.9872)
times_sq = SubwayStation("Times Square - 42nd Street", 40.7552, -73.9867)
canal_st = SubwayStation("Canal Street", 40.7195, -74.0014)
union_sq = SubwayStation("14th Street Union Square", 40.7347, -73.9904)
rock_ctr = SubwayStation("47th-50th Streets Rockefeller Center", 40.7587, -73.9815)
de_kal = SubwayStation("De Kalb Avenue", 40.6901, -73.9818)

subway_stations = [coney_island, j_st_metro_tech, w_4_st_wash_sq, one_four_5, herald_sq, times_sq, canal_st, union_sq, rock_ctr]
# Subway lines
line_f = SubwayLine("Line F")
line_ac = SubwayLine("Line_AC")
line_q = SubwayLine("Line_Q")
line_n = SubwayLine("Line_N")
subway_lines = [line_f, line_ac, line_q, line_n]

# Connecting stations with lines (sample connections)
coney_island.lines = [line_f, line_n, line_q]
j_st_metro_tech.lines = [line_f, line_ac]
w_4_st_wash_sq.lines = [line_ac, line_f]
one_four_5.lines = [line_ac]
herald_sq.lines = [line_f, line_q, line_n]
times_sq.lines = [line_n, line_q]
canal_st.lines = [line_n]
union_sq.lines = [line_q, line_n]
rock_ctr.lines = [line_f]
de_kal.lines = [line_q]

# Define transition probabilities and rewards for each station-line pair.
# The transition model will be a non-deterministic or probabilistic model
# that maps a (station, line) pair with a next station (s’) and a certain
# probability. Therefore, the commuter is not guaranteed to leave the station
# immediately because a certain line is chosen. This could be due to a traffic
# delay, signal malfunction, or any conceivable reason that makes this problem stochastic (as it is in real life).
transition_probs = {
    # From Coney Island
    (coney_island, line_f, j_st_metro_tech): 0.9,
    (coney_island, line_f, coney_island): 0.1,
    (coney_island, line_ac, herald_sq): 0.8,
    (coney_island, line_ac, coney_island): 0.2,
    (coney_island, line_q, canal_st): 0.9,
    (coney_island, line_q, coney_island): 0.1,
    # From Jay Street Metro Tech
    (j_st_metro_tech, line_f, coney_island): 0.7,
    (j_st_metro_tech, line_f, j_st_metro_tech): 0.3,
    (j_st_metro_tech, line_ac, herald_sq): 0.6,
    (j_st_metro_tech, line_ac, j_st_metro_tech): 0.4,
    # Continue with similar updates for other stations and lines...
}
# Rewards with distance-based adjustment
rewards = {
    (current_station, line, next_station): distance_adjustment
    for (current_station, line, next_station) in transition_probs.keys()
    for distance_adjustment in [
        -np.linalg.norm(np.array(next_station.grid_point) - np.array(current_station.grid_point)) / 10.0
    ]
}

# We selected an intermediate discount factor (around 0.5 to 0.8) to balance 
# the consideration of both short-term and long-term rewards.
discount_factor = 0.5  # Discount factor for future rewards

# Initialize value function for each state
V = {station: 0 for station in subway_stations}

# Define actions available at each state (station)
actions = {
    coney_island: [line for line in coney_island.lines],
    j_st_metro_tech: [line for line in j_st_metro_tech.lines],
    w_4_st_wash_sq: [line for line in w_4_st_wash_sq.lines],
    one_four_5: [line for line in one_four_5.lines],
    herald_sq: [line for line in herald_sq.lines],
    times_sq: [line for line in times_sq.lines],
    canal_st: [line for line in canal_st.lines],
    union_sq: [line for line in union_sq.lines],
    rock_ctr: [line for line in rock_ctr.lines],
    de_kal: [line for line in de_kal.lines],
}

# Value Iteration
converged = False
epsilon = 1e-6  # Convergence threshold

# Value Iteration
while not converged:
    delta = 0
    # Iterate over all states
    for s in subway_stations:
        old_value = V[s]
        # Calculate the maximum expected value for all actions in the current state
        max_expected_value = max(
            sum(
                transition_probs.get((s, a, s_prime), 0) *
                (rewards.get((s, a, s_prime), 0) +
                 discount_factor * V[s_prime])
                for s_prime in subway_stations
            )
            for a in actions[s]
        )
        # Update the value function for the current state
        V[s] = max_expected_value
        # Update the maximum change in the value function
        delta = max(delta, abs(old_value - V[s]))
    # Check for convergence
    if delta < epsilon:
        converged = True

# Extract the optimal policy
policy = {}
# Iterate over all states
for s in subway_stations:
    # Find the action that maximizes the expected value in the current state
    optimal_action = max(
        actions[s],
        key=lambda a: sum(
            transition_probs.get((s, a, s_prime), 0) *
            (rewards.get((s, a, s_prime), 0) + discount_factor * V[s_prime])
            for s_prime in subway_stations
        )
    )   
    # Update the policy for the current state
    policy[s] = optimal_action

# Define a dictionary that maps (station, subway line) pairs to next stations
next_station = {
    (coney_island, line_f): j_st_metro_tech,
    (coney_island, line_q): de_kal,
    (coney_island, line_n): canal_st,

    (j_st_metro_tech, line_f): coney_island,
    (j_st_metro_tech, line_f): w_4_st_wash_sq,
    (j_st_metro_tech, line_ac): w_4_st_wash_sq,
    
    (w_4_st_wash_sq, line_ac): j_st_metro_tech,
    (w_4_st_wash_sq, line_f): j_st_metro_tech,
    (w_4_st_wash_sq, line_ac): one_four_5,
    (w_4_st_wash_sq, line_f): herald_sq, 
    
    (one_four_5, line_ac): w_4_st_wash_sq,
    
    (herald_sq, line_f): w_4_st_wash_sq,
    (herald_sq, line_f): rock_ctr,
    (herald_sq, line_q): union_sq,
    (herald_sq, line_q): times_sq,
    (herald_sq, line_n): union_sq,
    (herald_sq, line_n): times_sq,

    (times_sq, line_q): herald_sq,
    (times_sq, line_n): herald_sq,

    (canal_st, line_q): union_sq,
    (canal_st, line_q): de_kal,
    (canal_st, line_n): coney_island,
    (canal_st, line_n): union_sq,
    
    (union_sq, line_q): canal_st,
    (union_sq, line_n): canal_st,
    (union_sq, line_q): herald_sq,
    (union_sq, line_n): herald_sq,   
    
    (rock_ctr, line_f): herald_sq,
    
    (de_kal, line_q): coney_island,
}

# Print the optimal policy from station_A to station_D
s = station_A
visited_stations = set()
while s != station_D:
    if s in visited_stations:
        print("Infinite loop detected in policy. Please check your MDP parameters.")
        break
    visited_stations.add(s)
    print(f"In {s}, take {policy[s]}")
    s = next_station[(s, policy[s])]