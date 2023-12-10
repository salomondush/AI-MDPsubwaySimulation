import random
import subway_class as sc
# Subway stations
station_A = sc.SubwayStation("Station A")
station_B = sc.SubwayStation("Station B")
station_C = sc.SubwayStation("Station C")
station_D = sc.SubwayStation("Station D")

# Subway lines
line_1 = sc.SubwayLine("Line 1")
line_2 = sc.SubwayLine("Line 2")
line_3 = sc.SubwayLine("Line 3")
line_4 = sc.SubwayLine("Line 4")
line_5 = sc.SubwayLine("Line 5")

# Connecting stations with lines (sample connections)
station_A.lines = [line_1, line_2, line_5]
station_B.lines = [line_1, line_3, line_4]
station_C.lines = [line_2, line_4]
station_D.lines = [line_3, line_5]

# Define transition probabilities and rewards for each station-line pair.
# The transition model will be a non-deterministic or probabilistic model
# that maps a (station, line) pair with a next station (s’) and a certain
# probability. Therefore, the commuter is not guaranteed to leave the station
# immediately because a certain line is chosen. This could be due to a traffic
# delay, signal malfunction, or any conceivable reason that makes this problem stochastic (as it is in real life).
transition_probs = {
    # From Station A
    (station_A, line_1, station_B): 0.9,
    (station_A, line_1, station_A): 0.1,
    (station_A, line_2, station_C): 0.9,
    (station_A, line_2, station_A): 0.1,
    (station_A, line_5, station_D): 0.9,
    (station_A, line_5, station_A): 0.1,
    # From Station B
    (station_B, line_1, station_A): 0.9,
    (station_B, line_1, station_B): 0.1,
    (station_B, line_3, station_D): 0.9,
    (station_B, line_3, station_B): 0.1,
    (station_B, line_4, station_C): 0.9,
    (station_B, line_4, station_B): 0.1,
    # From Station C
    (station_C, line_2, station_A): 0.9,  # Only one way from C to A
    (station_C, line_2, station_C): 0.1,
    (station_C, line_4, station_B): 0.9,
    (station_C, line_4, station_C): 0.1,
    # From Station D (Terminal state)
    (station_D, line_3, station_D): 1,  # Terminal state, no transition
}
# Rewards: (station, line, next_station) -> reward
# the reward for staying at the terminal/destination station is set to 0.
rewards = {
    # From Station A
    (station_A, line_1, station_B): 10,
    (station_A, line_5, station_D): 35,
    (station_A, line_2, station_C): -5,
    # From Station B
    (station_B, line_1, station_A): -5,
    (station_B, line_4, station_C): -5,
    (station_B, line_3, station_D): 20,
    # From Station C
    (station_C, line_2, station_A): 5,
    (station_C, line_4, station_B): 22,
    # From Station D (Terminal state)
    # Terminal state reward set to 0
    # (no additional reward for staying at terminal)
    (station_D, line_3, station_D): 0,
    (station_D, line_5, station_A): -5,
    (station_D, line_3, station_B): -5
}

# We selected an intermediate discount factor (around 0.5 to 0.8) to balance
# the consideration of both short-term and long-term rewards.
discount_factor = 0.5

# Initialize value function for each state
V = {station: 0 for station in [station_A, station_B, station_C, station_D]}

# Define actions available at each state (station)
actions = {
    station_A: [line for line in station_A.lines],
    station_B: [line for line in station_B.lines],
    station_C: [line for line in station_C.lines],
    station_D: [line for line in station_D.lines]
}

# Value Iteration
converged = False
epsilon = 1e-6  # Convergence threshold

# Value Iteration
while not converged:
    delta = 0
    # Iterate over all states
    for s in [station_A, station_B, station_C, station_D]:
        old_value = V[s]
        # Calculate the maximum expected value for all actions in the current state
        max_expected_value = max(
            sum(
                transition_probs.get((s, a, s_prime), 0) *
                (rewards.get((s, a, s_prime), 0) +
                 discount_factor * V[s_prime])
                for s_prime in [station_A, station_B, station_C, station_D]
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
for s in [station_A, station_B, station_C, station_D]:
    # Find the action that maximizes the expected value in the current state
    optimal_action = max(
        actions[s],
        key=lambda a: sum(
            transition_probs.get((s, a, s_prime), 0) *
            (rewards.get((s, a, s_prime), 0) + discount_factor * V[s_prime])
            for s_prime in [station_A, station_B, station_C, station_D]
        )
    )
    # Update the policy for the current state
    policy[s] = optimal_action

# Define a dictionary that maps (station, subway line) pairs to next stations
next_station = {
    (station_A, line_1): station_B,
    (station_A, line_2): station_C,
    (station_A, line_5): station_D,
    (station_B, line_1): station_A,
    (station_B, line_3): station_D,
    (station_B, line_4): station_C,
    (station_C, line_2): station_A,
    (station_C, line_4): station_B,
}

def random_traversal(start_station, end_station):
    current_station = start_station
    visited_stations = set()
    num_visits = 0

    while current_station != end_station:
        num_visits+=1
        if current_station in visited_stations:
            print("Infinite loop detected in traversal.")
            return [1, num_visits]
        visited_stations.add(current_station)
        possible_actions = actions[current_station]
        random_action = random.choice(possible_actions)

        print(f"In {current_station}, take {random_action}")

        current_station = next_station[(current_station, random_action)]
    return [2, num_visits]

def value_iter(start_station, end_station):
    current_station = start_station
    visited_stations = set()
    num_visits = 0
    while current_station != end_station:
        num_visits +=1
        if current_station in visited_stations:
            print("Infinite loop detected in policy. Please check your MDP parameters.")
            return [1, num_visits]
        visited_stations.add(current_station)
        print(f"In {current_station}, take {policy[current_station]}")
        current_station = next_station[(current_station, policy[current_station])]
    return [2, num_visits]