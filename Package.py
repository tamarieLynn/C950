# Tamarie Carrillo Student ID:011420359


# Used the given hash example changed from movie to package
# C950 - Webinar-2 - Getting Greedy, who moved my data?
# W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Ref: zyBooks: 3.3.1: MakeChange greedy algorithm.

class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status):
        # Initialize package attributes
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

    # Convert the package information to a string for easy printing
    def __str__(self):
        delivery_time_str = str(self.delivery_time) if self.delivery_time else "Not delivered"
        return "%s, %s,%s, %s,%s, %s,%s, %s, %s" % (
            self.ID, self.address, self.city, self.state, self.zipcode,
            self.deadline_time, self.weight, self.status, delivery_time_str)
