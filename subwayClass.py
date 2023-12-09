import math
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
    def __init__(self, name, delay_prob):
        self.name = name
        self.delay_prob =delay_prob

    def __str__(self):
        return self.name
    