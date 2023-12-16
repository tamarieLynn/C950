# Tamarie Carrillo Student ID:011420359


# Section A hash table without any additional libraries or classes
class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        # Initialize the hash table with an empty list for each bucket
        self.table = []
        for _ in range(initial_capacity):
            self.table.append([])

    def __str__(self):
        # Convert the hash table to a string for easy printing
        result = ""
        for bucket in self.table:
            if bucket:
                for key, value in bucket:
                    result += f"{key}: {value}\n"
        return result

    def insert(self, key, item):
        # Insert a key-value pair into the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for i, kv in enumerate(bucket_list):
            if kv[0] == key:
                # Update the value if the key already exists
                bucket_list[i] = (key, item)
                return
        # Add a new key-value pair if the key doesn't exist
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
        # Remove a key-value pair from the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return

    # added to be able to print all package at a specific time
    def get_all_keys(self):
        keys = []
        for bucket_list in self.table:
            for key, _ in bucket_list:
                keys.append(key)
        return keys

    # Used the given hash example
    # C950 - Webinar-2 - Getting Greedy, who moved my data?
    # W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
    # Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
    # Ref: zyBooks: 3.3.1: MakeChange greedy algorithm.
