import csv
import datetime


class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for _ in range(initial_capacity):
            self.table.append([])

    def __str__(self):
        result = ""
        for bucket in self.table:
            if bucket:
                for key, value in bucket:
                    result += f"{key}: {value}\n"
        return result

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for i, kv in enumerate(bucket_list):
            if kv[0] == key:
                bucket_list[i] = (key, item)
                return

        key_value = (key, item)
        bucket_list.append(key_value)

    # Check load factor and resize if necessary
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return

    def values(self):
        for bucket_list in self.table:
            for key, value in bucket_list:
                yield value

    def update(self, key, updated_item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for i, (existing_key, existing_item) in enumerate(bucket_list):
            if existing_key == key:
                bucket_list[i] = (key, updated_item)
                return

        # If key is not found, you can raise an exception or handle it accordingly
        raise KeyError(f"Key '{key}' not found in the hash table")


class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status):
        self.delivery_status = None
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.delivery_time = None
        self.departure_time = None

    def __str__(self):
        delivery_time_str = str(self.delivery_time) if self.delivery_time else "Not delivered"
        return "%s, %s,%s, %s,%s, %s,%s, %s, %s" % (
            self.ID, self.address, self.city, self.state, self.zipcode,
            self.deadline_time, self.weight, self.status, delivery_time_str)

    def update_status(self, convert_timedelta):
        try:
            # Ensure self.delivery_time and convert_timedelta are both not None
            if self.delivery_time and convert_timedelta:
                # Extract hours and minutes from convert_timedelta
                convert_hours, convert_minutes = divmod(convert_timedelta.seconds // 60, 60)

                # Extract hours and minutes from self.delivery_time
                delivery_hours, delivery_minutes = divmod(self.delivery_time.seconds // 60, 60)

                # Check if self.delivery_time is earlier than convert_timedelta
                if (delivery_hours, delivery_minutes) < (convert_hours, convert_minutes):
                    self.status = "Delivered"
                elif self.departure_time > convert_timedelta:
                    self.status = "En route"
                else:
                    self.status = "At Hub"
            else:
                raise ValueError("Error: Cannot update status. Delivery time or provided time is not available.")

            # Update the delivery_status dictionary
            self.delivery_status = {'status': self.status, 'delivery_time': self.delivery_time}
        except Exception as e:
            print(f"An error occurred: {e}")


class Truck:
    def __init__(self, truck_id, capacity, average_speed, load, package_ids, mileage, current_location, departure_time):
        self.truck_id = truck_id
        self.capacity = capacity
        self.average_speed = average_speed
        self.load = load
        self.package_ids = package_ids
        self.mileage = mileage
        self.current_location = current_location
        self.departure_time = departure_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.truck_id, self.capacity, self.average_speed, self.load,
                                                   self.package_ids, self.mileage, self.current_location,
                                                   self.departure_time)


# Read the file of distance information
with open("Distance_info.csv") as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)

# Read the file of address information
with open("Address_file.csv") as csvfile1:
    CSV_Address = csv.reader(csvfile1)
    CSV_Address = list(CSV_Address)

# Read the file of package information
with open("Package_info.csv") as csvfile2:
    CSV_Package = csv.reader(csvfile2)
    CSV_Package = list(CSV_Package)


def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        next(package_data)  # Skip header row
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            # Set a default delivery time
            pDelivery_time = "12:00 AM"

            # Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus)

            # Insert data into hash table
            package_hash_table.insert(pID, p)


# Method for finding distance between two addresses
def distance_in_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]
    return float(distance)


# time = distance/speed


# Method to get address number from string literal of address
def extract_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


# Create truck object truck1
truck1 = Truck(1, 16, 18, None, [31, 6, 25, 26, 16, 15, 14, 40, 20, 21, 1, 37, 29, 13, 30, 19], 0.0,
               "4001 South 700 East",
               datetime.timedelta(hours=8))

# Create truck object truck2
truck2 = Truck(2, 16, 18, None, [3, 18, 36, 38, 39, 33, 2, 4, 7, 5, 8, 22, 24, 35, 32, 34, 28], 0.0,
               "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Create truck object truck3
truck3 = Truck(3, 16, 18, None, [9, 10, 11, 12, 17, 23, 27], 0.0, "4001 South 700 East",
               datetime.timedelta(hours=10, minutes=20))

# Create hash table
package_hash_table = ChainingHashTable()

# Load packages into hash table
load_package_data("Package_info.csv", package_hash_table)


def delivering_packages(truck, package_hash_table):
    not_delivered = []
    for packageID in truck.package_ids:
        package = package_hash_table.search(packageID)
        not_delivered.append(package)

    truck.package_ids.clear()

    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None

        for package in not_delivered:
            distance = distance_in_between(extract_address(truck.current_location),
                                           extract_address(package.address))
            if distance <= next_address:
                next_address = distance
                next_package = package

        truck.package_ids.append(next_package.ID)
        not_delivered.remove(next_package)
        truck.mileage += next_address
        truck.current_location = next_package.address
        travel_time = truck.calculate_travel_time(next_address)

        truck.departure_time += travel_time
        next_package.delivery_time = truck.departure_time
        next_package.departure_time = truck.departure_time

        # Update the package in the hash table
        package_hash_table.update(next_package.ID, {'delivery_time': next_package.delivery_time})

        # Call update_status to update the status based on the new delivery time
        next_package.update_status(next_package.delivery_time)

        print(next_package.delivery_time, next_package)


def get_user_input_time():
    while True:
        try:
            user_input = input("Enter the time in HH:MM AM/PM format: ")
            time_format = "%I:%M %p"
            parsed_time = datetime.datetime.strptime(user_input, time_format).time()
            return parsed_time
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM AM/PM format.")


def get_delivery_status(package_id, user_time, package_hash_table):
    try:
        # Get the package from the hash table
        package = package_hash_table.search(package_id)

        # Check if the package exists
        if not package:
            return {"error": f"Package with ID {package_id} not found."}

        # Update the package status based on the provided time
        package.update_status(user_time)

        # Return the package information including the updated status
        return {"package_info": f"Package {package_id} - {str(package)}"}

    except ValueError:
        return {"error": "Invalid time format. Please enter the time in HH:MM AM/PM format."}


# use to print all package data, used WGU movie data example
def get_package_data():
    print("Package Information from HashTable:")
    for bucket in package_hash_table.table:
        for kv in bucket:
            print("Package: {}".format(kv[1]))


def display_truck_information():
    # print("\nTotal Mileage Traveled by all Trucks: {total_mileage} miles\n".format(total_mileage=get_total_mileage()))
    print(truck1.mileage + truck2.mileage + truck3.mileage)


# UI start include delivery time and weight
def get_user_input():
    try:
        package_id = int(input("Enter the package ID: "))
        return package_id
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return None


def home_page():
    load_package_data("Package_info.csv", package_hash_table)
    # load_trucks(truck_data, package_hash_table)

    while True:
        print("Select from the following: "
              "\n1 - Delivery Status"  # Delivery status must include the time.
              "\n2 - Print all packages"
              "\n3 - Display truck mileage total"
              "\n4 - End program")

        choice = input("Enter your choice: ")

        if choice == '1':
            package_id = get_user_input()
            if package_id is not None:
                # Get user input for time
                user_time = get_user_input_time()

                # Use the get_delivery_status function
                result = get_delivery_status(package_id, user_time, package_hash_table)

                if "error" in result:
                    print(result["error"])
                else:
                    print("Package Information:")
                    package_info = result["package_info"]
                    print(package_info)
                    # Display delivery time if available
                    delivery_time = result.get('delivery_status', {}).get('delivery_time')
                    if delivery_time:
                        print(f"Delivery Time: {delivery_time}")

        elif choice == '2':
            get_package_data()

        elif choice == '3':
            display_truck_information()
            pass

        elif choice == '4':
            print("Ending program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


home_page()
