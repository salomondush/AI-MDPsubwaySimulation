import subwaySimulation as ss
import numpy as np

def get_start_station():
    print("Available stations:")
    for i, station in enumerate([ss.station_A, ss.station_B, ss.station_C, ss.station_D], start=1):
        print(f"{i}. {station.name}")

    while True:
        try:
            choice = input("Enter the number of the starting station (or 'q' to exit): ")

            if choice.lower() == 'q':
                exit()  # Call exit() function to exit the program

            choice = int(choice)
            if 1 <= choice <= 4:
                return [ss.station_A, ss.station_B, ss.station_C, ss.station_D][choice - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_user_choice():
    while True:
        print("Choose an action:")
        print("1. Perform random traversal")
        print("2. Perform MDP value iteration")
        print("q. Exit")
        choice = input("Enter your choice (1, 2, or q): ")

        if choice == "1":
            return "random"
        elif choice == "2":
            return "value_iteration"
        elif choice == "q":
            exit()  # Call exit() function to exit the program
        else:
            print("Invalid choice. Please enter 1, 2, or q.")

def test_mode():
    start_station = get_start_station()
    iteration_type = get_user_choice()
    num_station_visits = []  # add num of visits to each
    success_rate = []  # add 1 if fail, add 2 if succeed

    try:
        num_iterations = int(input("Enter the number of times to run the model: "))
    except ValueError:
        print("Invalid input. Defaulting to 1 iteration.")
        num_iterations = 1

    for _ in range(num_iterations):
        if iteration_type == "random":
            print(f"Starting random traversal from {start_station.name} to {ss.station_D.name}")
            result = ss.random_traversal(start_station, ss.station_D)
            success_rate.append(result[0])
            num_station_visits.append(result[1])
        elif iteration_type == "value_iteration":
            result = ss.value_iter(start_station, ss.station_D)
            success_rate.append(result[0])
            num_station_visits.append(result[1])

    print(f"Test Mode Results for {iteration_type} from {start_station.name} to {ss.station_D.name}")
    print(f"Average Number of Station Visits: {np.mean(np.array(num_station_visits))}")
    print(f"Goal State Success Rate: {(success_rate.count(2) / len(success_rate))*100}")

if __name__ == "__main__":
    while True:
        mode_choice = input("Choose the mode \n1. Test \n2. Normal\nEnter the mode or press 'q' to quit ").lower()
        if mode_choice == "1":
            test_mode()
        elif mode_choice == "2":
            start_station = get_start_station()
            end_station = ss.station_D
            model_mode = get_user_choice()
            if model_mode == "random":
                print(f"Starting random traversal from {start_station.name} to {end_station.name}")
                ss.random_traversal(start_station, end_station)
            elif model_mode == "value_iteration":
                ss.value_iter(start_station, end_station)
        elif mode_choice == 'q':
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or q.")
