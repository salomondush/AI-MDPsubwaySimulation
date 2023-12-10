# Subway Simulation

The `subwaySimulation.py`script is a Python program that simulates a subway system using Markov Decision Processes (MDP). The subway system consists of four stations (Station A, Station B, Station C, Station D) and five subway lines (Line 1, Line 2, Line 3, Line 4, Line 5).

## Subway System Structure

The subway system is structured as follows:

- Station A is connected to Station B via Line 1, Station C via Line 2, and Station D via Line 5.
- Station B is connected to Station A via Line 1, Station C via Line 4, and Station D via Line 3.
- Station C is connected to Station A via Line 2 and Station B via Line 4.
- Station D is connected to Station A via Line 5 and Station B via Line 3.


The connections can be visualized as follows:

```
Station A -- Line 1 --> Station B
       | -- Line 2 --> Station C
       | -- Line 5 --> Station D
       
Station B -- Line 1 --> Station A
       | -- Line 3 --> Station D
       | -- Line 4 --> Station C
       
Station C -- Line 2 --> Station A
       | -- Line 4 --> Station B

Station D -- Line 5 --> Station A
       | -- Line 3 --> Station B
```

## Simulation Process

The simulation process uses Value Iteration to find the optimal policy for moving from one station to another. The policy is a mapping from each station to the subway line that provides the highest expected value.

The expected value for each action (subway line) in each state (station) is calculated based on transition probabilities, rewards, and a discount factor. The transition probabilities represent the likelihood of moving from one station to another via a particular subway line. The rewards represent the benefit of moving from one station to another via a particular subway line.

The commuter is not guaranteed to leave the station immediately because a certain line is chosen. For example, if a commuter plans to go from Station A to Station B through line 1, there's a 0.9 chance that it happens, but also a 0.1 chance that they stay at Station A. This could be due to a traffic delay, signal malfunction, or any conceivable reason that makes this problem stochastic (as it is in real life).

The reward values are chosen to reflect the desirability of each action. Staying at the same station (due to a delay, for example) is given a reward of 0, as it neither helps nor hinders the commuter's progress. Moving backwards is given a negative reward, as it moves the commuter further from their destination. Moving forwards is given a positive reward, as it moves the commuter closer to their destination. Shorter paths are given higher total rewards than longer paths, as they allow the commuter to reach their destination more quickly.

Once the optimal policy is found, the simulation prints the optimal route from Station A to Station D.

## Example Runs

- From Station A to Station D: In Station A, take Line 5
- From Station C to Station D: In Station C, take Line 4, then in Station B, take Line 3

## Running the Simulation

To run the simulation:
- To run a test, run 'python3 subway_client.py' and choose test mode. Select the iteration type, start station, and number of runs you want the model to simulate. This will give you the average number of station visits, and goal state success rate.
- To run a test, run 'python3 subway_client.py' and choose normal mode. Select the iteration type and the start station according to the client. It will give you the optimal path.
## Note

This is a simple simulation and does not account for real-world complexities such as varying travel times, delays, or service disruptions. It is intended for educational purposes to demonstrate the concept of Markov Decision Processes.
