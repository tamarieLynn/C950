# Tamarie Carrillo Student ID:011420359

import csv
import datetime
from Truck import Truck
from HashTable import ChainingHashTable
import Package

# Sources used on this file
# https://realpython.com/knn-python/
# https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
# https://docs.python.org/3/library/csv.html?highlight=csv
# csv — CSV File Reading and Writing
# Source code: Lib/csv.py
# Read the file of distance information
with open("Distance.csv") as csvfile:
    distance_csv = csv.reader(csvfile)
    distance_csv = list(distance_csv)

# Read the file of address information
with open("Address.csv") as csvfile:
    address_csv = csv.reader(csvfile)
    address_csv = list(address_csv)

# Read the file of package information
with open("Packages.csv") as csvfile:
    package_csv = csv.reader(csvfile)
    package_csv = list(package_csv)


# I used the course webinars and the provided code changing for their example with movies to 
# packages, course instructor recommended doing this
def load_package_data(filename, package_hash_table):
    # Open the package information file
    with open(filename) as package_info:
        # Read the CSV data
        package_data = csv.reader(package_info)
        next(package_data)  # Skip header row
        # Iterate over each package in the CSV data
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            # Package object
            p = Package.Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus)

            # Insert data into hash table
            package_hash_table.insert(pID, p)


# this is used in the below algorithm for finding distance between two 
# addresses this will be what is compared to find the shortest distance
def get_the_distance_from_package(x_value, y_value):
    # Get distance from the Distance_info CSV
    distance = distance_csv[x_value][y_value]
    if distance == '':
        # If the distance is not available, try the reverse
        distance = distance_csv[y_value][x_value]
    return float(distance)


# Needed to fix type error and get address
def get_address(address):
    for row in address_csv:
        if address in row[2]:
            return int(row[0])


# Create truck objects with the packages I chose to meet the requirements outlined in PA. I provided screen clippings
# of the written work done to decide which packages need to go on which truck
truck1 = Truck(1, 16, 18, None, [31, 6, 25, 26, 16, 15, 14, 40, 20, 21, 1, 37, 29, 13, 30, 19], 0.0,
               "4001 South 700 East",
               datetime.timedelta(hours=8))

truck2 = Truck(2, 16, 18, None, [3, 18, 36, 38, 39, 33, 2, 4, 7, 5, 8, 22, 24, 35, 32, 34, 28], 0.0,
               "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

truck3 = Truck(3, 16, 18, None, [9, 10, 11, 12, 17, 23, 27], 0.0, "4001 South 700 East",
               datetime.timedelta(hours=10, minutes=20))
# set the departure times to work with the given set of restraints
truck1.departure_time = datetime.timedelta(hours=8, minutes=5)
truck2.departure_time = datetime.timedelta(hours=8, minutes=5)
truck3.departure_time = datetime.timedelta(hours=10, minutes=20)
trucks = [truck1, truck2, truck3]

# this is using the hash table method I created to access the package info from the csv files  
package_hash_table = ChainingHashTable()
# Load packages into hash table
load_package_data("Packages.csv", package_hash_table)


# below is a version of the nearest neighbor algorithm to find the most optimal route for the truck objects created 
# above.
def nearest_neighbor(truck, package_hash_table):
    not_delivered = []

    # Helper function to calculate delivery time based on travel time
    def find_truck_travel_time(travel_time):
        return truck.departure_time + travel_time

        # Helper function to parse time in "HH:MM AM/PM" format to datetime.timedelta

    def convert_time(time_str):
        time_format = "%I:%M %p"
        parsed_time = datetime.datetime.strptime(time_str, time_format).time()
        return datetime.timedelta(hours=parsed_time.hour, minutes=parsed_time.minute)

    for packageID in truck.package_ids:
        package = package_hash_table.search(packageID)
        not_delivered.append(package)

    # Clear the package IDs from the truck, as they will be reloaded
    truck.package_ids.clear()

    # Loop until all packages are delivered
    while len(not_delivered) > 0:
        # Find the next package with the closest distance to the truck's current location
        next_address = 2000
        next_package = None

        for package in not_delivered:
            distance = get_the_distance_from_package(get_address(truck.current_location),
                                                     get_address(package.address))
            if distance <= next_address:
                next_address = distance
                next_package = package

        # Load the next package onto the truck
        truck.package_ids.append(next_package.ID)
        # Remove from the list up top so the package is not checked again
        not_delivered.remove(next_package)
        # keep track of the mileage to make sure under 140
        truck.mileage += next_address
        # move truck to next location
        truck.current_location = next_package.address
        # Calculate travel time for the truck to reach the next delivery location
        # Use the info to figure out what time each package will be delivered to display in UI

        travel_time = truck.calculate_travel_time(next_address)

        # Update the truck's departure time and the package's delivery time
        truck.departure_time += travel_time
        next_package.delivery_time = find_truck_travel_time(travel_time)
        next_package.departure_time = truck.departure_time

        # Convert deadline_time to datetime.timedelta
        next_package_deadline_time = convert_time(next_package.deadline_time)

        # Update the package status directly, this is to make sure the status of package
        # is up-to-date, cannot figure out if this could be used instead of lookup in UI
        if next_package_deadline_time is not None:
            if next_package.delivery_time < next_package_deadline_time:
                next_package.status = "Delivered"
            elif truck.departure_time > next_package_deadline_time:
                next_package.status = "En route"
            else:
                next_package.status = "At Hub"


# THis is just to preview the truck routes produced in algo, I left it in the show when program runs
def print_truck_routes(trucks):
    for truck in trucks:
        print(f"Truck {truck.truck_id} Route: {truck.get_route()}, Mileage: {truck.mileage} miles")


# Put the trucks through the loading process
nearest_neighbor(truck1, package_hash_table)
nearest_neighbor(truck2, package_hash_table)
nearest_neighbor(truck3, package_hash_table)

print_truck_routes(trucks)
print(("Total miles traveled: ", truck3.mileage + truck2.mileage + truck1.mileage))
