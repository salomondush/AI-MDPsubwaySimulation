import math
def calculate_grid_point(lat, long):
    # Convert geographical coordinates to grid points (example using haversine formula)
    R = 6371  # Earth radius in kilometers
    lat_rad = math.radians(lat)
    lon_rad = math.radians(long)
    
    x = R * math.cos(lat_rad) * math.cos(lon_rad)
    y = R * math.cos(lat_rad) * math.sin(lon_rad)

    return x, y
print(f"Times Square:{calculate_grid_point(40.75605614948771, -73.98710391552848)}, Union Square:{calculate_grid_point(40.73467894122143, -73.99035475962178)}, J Street:{calculate_grid_point(40.69204758503175, -73.98498376782335)}")
