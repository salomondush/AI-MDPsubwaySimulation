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
coney_island = SubwayStation("Coney Island Station", 40.577760430189656, -73.97999295649412)
j_st_metro_tech = SubwayStation("Jay Street Metro Tech Station", 40.69204758503175, -73.98498376782335)
w_4_st_wash_sq = SubwayStation("West 4th Street Washington Square", 40.73253311848584, -74.00044235617023)
one_four_5 = SubwayStation("145th Street", 40.83419374298584, -73.94926049155865)
herald_sq = SubwayStation("34th Street Herald Square", 40.749842751497916, -73.98762350805688)
times_sq = SubwayStation("Times Square - 42nd Street", 40.75605614948771, -73.98710391552848)
canal_st = SubwayStation("Canal Street", 40.719700439317876, -74.00143758220091)
union_sq = SubwayStation("14th Street Union Square", 40.73467894122143, -73.99035475962178)
rock_ctr = SubwayStation("47th-50th Streets Rockefeller Center", 40.759045012104984, -73.98108954399662)
de_kal = SubwayStation("De Kalb Avenue", 40.69182616993852, -73.97380877906623)

subway_stations = [coney_island, j_st_metro_tech, w_4_st_wash_sq, one_four_5, herald_sq, times_sq, canal_st, union_sq, rock_ctr, de_kal]
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

# Define speed for each line (in km/h)
line_speeds = {
    line_f: 30,
    line_ac: 25,
    line_q: 20,
    line_n: 22,
}

rewards = {
    (current_station, line, next_station): distance_adjustment
    for (current_station, line, next_station) in transition_probs.keys()
    for distance_adjustment in [
        -np.linalg.norm(np.array(next_station.grid_point) - np.array(current_station.grid_point)) / 10.0
    ]
}

# Define a dictionary that maps (station, subway line) pairs to rewards including both speed-based and distance-based adjustments
combined_rewards = {
    (current_station, line, next_station): speed_reward + distance_adjustment
    for (current_station, line, next_station) in transition_probs.keys()
    for speed_reward, calculate_distance_adjustment in [
        (speed / 10.0, lambda: -np.linalg.norm(np.array(next_station.grid_point) - np.array(current_station.grid_point)) / 10.0)
    ]
}
# Example usage
for key, value in combined_rewards.items():
    print(f"From {key[0]} to {key[2]} on {key[1]}: Reward = {value}")
