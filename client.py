import subwaySimulation as ss
# Get user input for start station

def get_user_input():
    print("Available stations:")
    for idx, station in enumerate(ss.subway_stations, start=1):
        print(f"{idx}. {station}")

    start_idx = int(input("Enter the number of the starting station: ")) - 1
    end_idx = int(input("Enter the number of the ending station: ")) - 1

    return ss.subway_stations[start_idx], ss.subway_stations[end_idx]


def select_station(prompt):
    print(prompt)
    for idx, station in enumerate(ss.subway_stations, start=1):
        print(f"{idx}. {station}")

    selected_idx = int(input("Enter the number of the station: ")) - 1
    return ss.subway_stations[selected_idx]


def main():
    print("Welcome to the Subway Route Planner!")

    start_station = select_station("Select the starting station:")
    end_station = select_station("Select the ending station:")

    print(f"\nYou chose to travel from {start_station} to {end_station}.")

if __name__ == "__main__":
    main()
