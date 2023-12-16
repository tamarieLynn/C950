# Tamarie Carrillo Student ID:011420359

import datetime
from datetime import timedelta


# Used the given hash example, changed from movie to truck, same idea..
# C950 - Webinar-2 - Getting Greedy, who moved my data?
# W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Ref: zyBooks: 3.3.1: MakeChange greedy algorithm.
class Truck:
    def __init__(self, truck_id, capacity, average_speed, load, package_ids, mileage, current_location, departure_time):
        # Initialize truck attributes
        self.truck_id = truck_id
        self.capacity = capacity
        self.average_speed = average_speed
        self.load = load
        self.package_ids = package_ids
        self.mileage = mileage
        self.current_location = current_location
        self.departure_time = departure_time

    def __str__(self):
        # Convert truck information to a string for easy printing
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.truck_id, self.capacity, self.average_speed, self.load,
                                                   self.package_ids, self.mileage, self.current_location,
                                                   self.departure_time)

    def calculate_travel_time(self, distance):
        # Calculate travel time based on the provided distance and average speed
        return datetime.timedelta(hours=distance / self.average_speed)

    def get_route(self):
        # Return a copy of the package_ids list
        return list(self.package_ids)
