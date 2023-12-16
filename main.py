# Tamarie Carrillo Student ID:011420359


# Had to do the import statement from import to get strptime to work reference used https://stackoverflow.com
# /questions/12070193/why-does-trying-to-use-datetime-strptime-result-in-module-object-has-no-at
from datetime import datetime, timedelta
from NearestNeighbor import truck1, truck2, truck3, package_hash_table


# Documents used for this page https://docs.python.org/3/library/datetime.html

# Section B: this is a required function for the PA, needs to print up all package info
# I originally planned to use it to find package status at specific time but ended up making new method for that
def look_up(package_id):
    package = package_hash_table.search(package_id)
    print(package_id)

    if package:
        print("Package Status:")
        print(f"Package ID: {package.ID}")
        print(f"Status: {package.status}")
        print(f"Delivery address: {package.address}")
        print(f"Delivery city: {package.city}")
        print(f"Delivery zip code: {package.zipcode}")
        print(f"Package weight: {package.weight}")
        print(f"Delivery deadline: {package.deadline_time}")

        if package.delivery_time:
            print(f"Delivered at: {package.delivery_time}")

        else:
            print(f"Estimated delivery time: {package.departure_time}")
            current_location = truck1.current_location
            package_address = package.address
            delivery_deadline = package.delivery_deadline
            package_weight = package.weight

            print(f"Current location: {current_location}")
            print(f"Package address: {package_address}")
            print(f"Delivery deadlineL {delivery_deadline}")
            print(f"Package weight: {package_weight}")

    else:
        print(f"Package with ID {package_id} not found.")


# Section B: Menu for UI section
def display_menu():
    print("1. View all packages status and total miles")
    print("2. View all package status at a specific time")
    print("3. Check delivery status at a specific time")
    print("4. Exit")


# single package delivery time not used for specific times user # 1
def view_package_status():
    for package_id in package_hash_table.get_all_keys():
        package = package_hash_table.search(package_id)

        if package is not None:
            print(f"\nPackage Status for Package ID {package_id}:")
            print(f"Status: {package.status}")


# This is working to view truck mileage if user chose 1
def view_total_mileage():
    total_mileage_all_trucks = truck1.mileage + truck2.mileage + truck3.mileage
    print(f"Total mileage traveled by all trucks: {total_mileage_all_trucks} miles")


# This is working to get user input for section D interface,
# if user chooses 3
# TypeError: '<' not supported between instances of 'datetime.timedelta' and 'datetime.datetime'
# Also %H = 24 - %I = 12 hour
def check_delivery_status_at_specific_time():
    package_id = int(input("Enter the package ID: "))
    specific_time = input("Enter the specific time (HH:MM AM/PM): ")
    # figured out you need am/pm and this %p or 05 pm will be less than 09 am...
    user_time = datetime.strptime(specific_time, "%I:%M %p").time()
    user_time = timedelta(hours=user_time.hour, minutes=user_time.minute, seconds=user_time.second)
    package = package_hash_table.search(package_id)
    delivery_hours = package.delivery_time
    package = package_hash_table.search(package_id)

    if package is not None:
        if user_time > delivery_hours:
            print("Delivered")
        elif package.departure_time < user_time < package.delivery_time:
            print("En route")
        else:
            print("At Hub")


# This works to display all package statuses at a specific time use #2
def check_status_of_all_packages_at_specific_time(package_hash_table):
    specific_time = input("Enter the specific time (HH:MM AM/PM): ")
    user_time = datetime.strptime(specific_time, "%I:%M %p").time()
    user_time = timedelta(hours=user_time.hour, minutes=user_time.minute, seconds=user_time.second)

    for package_id in package_hash_table.get_all_keys():
        package = package_hash_table.search(package_id)
        delivery_hours = package.delivery_time

        if package is not None:
            print(f"\nPackage Status for Package ID {package_id}:", f" Delivery Time: {package.delivery_time}")
            # Print statements to check status correctness
            print(package.address, package.city, package.state, package.zipcode, package.weight)
            # print(f"Delivery deadline: {package.deadline_time}")
            # print(f"Delivery Time: {package.delivery_time}")

            if package is not None:
                if user_time > delivery_hours:
                    print("Delivered")
                elif package.departure_time < user_time < package.delivery_time:
                    print("En route")
                else:
                    print("At Hub")


# This method is for producing the screenshots need for section D. 1, 2, 3 - ended up not using
# Needed to add minutes to accurate results
# def print_all_packages():
#     # I included the packages at 8 even though the PA did not need it just so it shows all packages loaded as some
#     # are delivered and not on the trucks by 9am. There will be repeated packages as they will stay on the same truck
#     # until delivered. Some packages will be printed on truck 1 or 2 or 3 for each time section. I rearanged how it
#     # prints so all of the times are now printing together.
#     print("Packages on truck1 at 8:")
#     for package_id in truck1.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 8 or (hours == 8 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck2 at 8:")
#     for package_id in truck2.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 8 or (hours == 8 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck3 at 8:")
#     for package_id in truck3.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 8 or (hours == 8 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck1 at 9:")
#     for package_id in truck1.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 9 or (hours == 9 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck2 at 9:")
#     for package_id in truck2.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 9 or (hours == 9 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck3 at 9:")
#     for package_id in truck3.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 9 or (hours == 9 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck1 at 10:")
#     for package_id in truck1.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 10 or (hours == 10 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck2 at 10:")
#     for package_id in truck2.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 10 or (hours == 10 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck3 at 10:")
#     for package_id in truck3.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 10 or (hours == 10 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck1 at 12:")
#     for package_id in truck1.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 12 or (hours == 12 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck2 at 12:")
#     for package_id in truck2.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 12 or (hours == 12 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck3 at 12:")
#     for package_id in truck3.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours > 12 or (hours == 12 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck1 at 1:")
#     for package_id in truck1.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours < 1 or (hours == 1 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck2 at 1:")
#     for package_id in truck2.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours < 1 or (hours == 1 and minutes > 00):
#                 print(package)
#
#     print("Packages on truck3 at 1:")
#     for package_id in truck3.package_ids:
#         package = package_hash_table.search(package_id)
#         if package and package.delivery_time:
#             delivery_hours = package.delivery_time
#             hours = delivery_hours.total_seconds() // 3600
#             minutes = (delivery_hours.total_seconds() % 3600) // 60
#             # why does this have > not <
#             if hours < 1 or (hours == 1 and minutes > 00):
#                 print(package)


# This is the method to call to get user input and return expected values.
while True:
    display_menu()
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        view_total_mileage()
        view_package_status()
    elif choice == '2':
        check_status_of_all_packages_at_specific_time(package_hash_table)
    elif choice == '3':
        check_delivery_status_at_specific_time()
    elif choice == '4':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")

# to check the look-up function works, will run after the UI finishes.
print(look_up(23))
