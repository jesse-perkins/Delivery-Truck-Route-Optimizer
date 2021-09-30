from dataStructures.hashtable import HashTable
from model.truck import Truck
from model.package import Package
import datetime


class Facility:
    """A class used to represent a Shipping Facility

    **Class Attributes**
        *DEFAULT_EOD* (datetime):
            The default timestamp for the end of the day.

    **Instance Attributes**
        *all_trucks* ([Truck]):
            The list of all trucks.
        *all_packages* (HashTable(Packages)):
            The list of all packages.
        *all_addresses* ([str]):
            The list of all addresses. Indices match to all_distances.
        *all_distances* ([[float]]):
            The list of all distances. Indices match to all_addresses.
        *unassigned_packages* ([Packages]):
            The list of all packages that have yet to be assigned to a truck.
    **Methods**
        *__init__* () -> (None)
            - TIME: O(f(x))= n^2
            - SPACE: O(f(x))= n^2
        *preload* () -> (None)
            - TIME: O(f(x))= n^2
            - SPACE: O(f(x))= n^2
        *loader* (truck (Truck), remaining_packages ([Package])) -> [Package]
            - TIME: O(f(x))= n^2
            - SPACE: O(f(x))= n^2
        *delivery* (truck: Truck) -> (None)
            - TIME: O(f(x))= n^2
            - SPACE: O(f(x))= n^2
        *nearest_location* (current_address_index (int), target_address_indices ([int])) -> (int)
            - TIME: O(f(x))= n
            - SPACE: O(f(x))= n
    """

    DEFAULT_EOD: datetime.datetime = datetime.datetime.now().replace(hour=23, minute=59, second=0)

    def __init__(self) -> None:
        """*__init__*
            Parses data from the data files to provide storage for packages, addresses, lists of distances, and trucks.
            The trucks are not loaded as of yet.

            TIME: O(f(x))= n^2

            SPACE: O(f(x))= n^2

        :return: (None)
        """
        # Create the trucks.
        self.all_trucks = []
        count = 0
        while count < 3:
            self.all_trucks.append(Truck())
            count += 1
        # Read in the package data and create the all_packages HashTable
        with open("dataFiles/PackageInfo.csv") as source_csv_file:
            line_count = 0
            self.unassigned_packages = []
            for line in source_csv_file:
                line_count += 1
                package_data = line.split(",")
                new_package_id = int(package_data[0])
                new_package_address = package_data[1]
                new_package_city = package_data[2]
                # Skipped state as it is not needed
                new_package_zipcode = int(package_data[4])
                # Parse delivery deadline data
                if package_data[5] != "EOD":
                    string_time_split_1: [str] = package_data[5].split(':')
                    string_time_split_2: [str] = string_time_split_1[1].split()
                    hours = int(string_time_split_1[0])
                    if string_time_split_2[1] == "PM" and hours != 12:
                        hours += 12
                    minutes = int(string_time_split_2[0])
                    new_package_time_clock = datetime.datetime.now().replace(hour=hours, minute=minutes, second=0)
                else:
                    new_package_time_clock = Facility.DEFAULT_EOD
                # Continue with assignments
                new_package_weight = float(package_data[6])
                new_package_note = package_data[7]
                new_package_note = new_package_note.rstrip()
                new_package = Package(new_package_id,
                                      new_package_address,
                                      new_package_city,
                                      new_package_zipcode,
                                      new_package_time_clock,
                                      new_package_weight,
                                      new_package_note
                                      )
                self.unassigned_packages.append(new_package)
            self.all_packages = HashTable(line_count)
            for package in self.unassigned_packages:
                self.all_packages.insert(package.package_id, package)
        source_csv_file.close()
        # Read in the distance data and create the addresses and distances lists
        with open("dataFiles/LocationDistanceChart.csv") as source_csv_file:
            self.all_addresses = []
            self.all_distances = []
            line_count = 0
            for line in source_csv_file:
                line_count += 1
                line = line.rstrip()
                split_line = line.split(',')
                self.all_addresses.append(split_line[0])
                split_line.pop(0)
                distances = []
                for distance in split_line:
                    distances.append(float(distance))
                self.all_distances.append(distances)
        return

    def preload(self) -> None:
        """*preload*
            Sifts through the packages and preloads packages into trucks based on:
                1) package availability (late arrival / wrong address)
                2) delivery deadline
                3) notes
                4) addresses matching

            TIME: 0(f(x))= n^2

            SPACE: O(f(x))= n^2

        :return: (None)
        """
        # Preload trucks based on notes and matching addresses
        delivered_together = [13, 14, 15, 16, 19, 20]
        for package in self.unassigned_packages.copy():
            if package.package_id in delivered_together:
                self.all_trucks[0].package_list.insert(package.package_id, package)
            elif package.note == "Can only be on truck 2" or package.note == "Wrong address listed":
                self.all_trucks[1].package_list.insert(package.package_id, package)
            elif package.note.startswith("Delayed"):
                self.all_trucks[2].package_list.insert(package.package_id, package)
                self.all_trucks[2].current_time = datetime.datetime.now().replace(hour=9, minute=5, second=0)
                self.all_trucks[2].departure_time = self.all_trucks[2].current_time
        # Preload packages that match preloaded addresses, but that aren't time restricted
        for truck in self.all_trucks:
            for loaded_package in truck.package_list.get_values():
                for unassigned_package in self.unassigned_packages:
                    if unassigned_package.address == loaded_package.address \
                            and unassigned_package.deadline == Facility.DEFAULT_EOD \
                            and truck.package_list.lookup(unassigned_package.package_id) is None:
                        truck.package_list.insert(unassigned_package.package_id, unassigned_package)
        # Clear assigned packages from unassigned list
        for truck in self.all_trucks:
            for package in truck.package_list.get_values():
                if package in self.unassigned_packages:
                    self.unassigned_packages.remove(package)

    def loader(self, truck: Truck, remaining_packages: [Package]) -> [Package]:
        """*loader*
            Takes a truck and the packages remaining to be assigned and uses the nearest location
            function to selectively load them into the truck, then returns any unassigned packages.

            TIME: O(f(x))= n^2

            SPACE: O(f(x))= n^2

        :param truck: (Truck) The truck to be loaded with packages
        :param remaining_packages: ([Package]) The list of packages to be loaded
        :return: ([Package]) Leftover packages that did not get loaded
        """
        # Start at the hub, with the indices for the remaining packages as the targets for the greedy algorithm
        address_index = 0
        target_address_indices = []
        for package in truck.package_list.get_values():
            remaining_packages.append(package)
        for package in remaining_packages:
            target_address_indices.append(self.all_addresses.index(package.address))
        # Decide the next stop using a recursive call that either fills the truck or assigns all remaining packages
        while truck.package_list.item_count < 16 and len(remaining_packages) > 0:
            address_index = self.nearest_location(address_index, target_address_indices)
            target_address_indices.remove(address_index)
            address = self.all_addresses[address_index]
            for package in remaining_packages:
                if package.address == address:
                    if truck.package_list.lookup(package.package_id) is None:
                        truck.package_list.insert(package.package_id, package)
                    remaining_packages.remove(package)
                    break
        # Remove assigned packages from the remaining packages list and return.
        for package in truck.package_list.get_values():
            if package in remaining_packages:
                remaining_packages.remove(package)
        return remaining_packages

    def delivery(self, truck: Truck) -> None:
        """*delivery*
            Iterates through packages on a truck, marks packages as delivered, and issues a timestamp.

            TIME: O(f(x))= n^2

            SPACE: O(f(x))= n^2

        :param truck: (Truck) The truck to deliver packages
        :return: (None)
        """
        # Set the current index to the hub and determine the next address, then launch a while loop that ends when the
        # truck is out of boxes. Mark delivery time and delivery status as well.
        current_address_index = 0
        target_address_list = []
        for package in truck.package_list.get_values():
            target_address_list.append(self.all_addresses.index(package.address))
        count = 0
        while count < truck.package_list.item_count:
            count += 1
            next_address_index = self.nearest_location(current_address_index, target_address_list)
            distance = self.all_distances[current_address_index][next_address_index]
            seconds_travelling = distance / (Truck.MILES_PER_HOUR / 60 / 60)
            truck.miles_traveled += distance
            truck.current_time = truck.current_time + datetime.timedelta(seconds=seconds_travelling)
            current_address_index = next_address_index
            target_address_list.remove(next_address_index)
            for package in truck.package_list.get_values():
                if package.address == self.all_addresses[current_address_index]:
                    package.delivery_time_stamp = truck.current_time
                    package.delivery_status = True
        # Add in returning to the hub from the last address.
        distance = self.all_distances[current_address_index][0]
        seconds_travelling = distance / (Truck.MILES_PER_HOUR / 60 / 60)
        truck.miles_traveled += distance
        truck.current_time = truck.current_time + datetime.timedelta(seconds=seconds_travelling)

    def nearest_location(self, current_address_index: int, target_address_indices: [int]) -> int:
        """*nearest_location*
            Determines the nearest node to the current node.

            TIME: O(f(x))= n

            SPACE: O(f(x))= n

        :param current_address_index: (int) The index which of the current address
        :param target_address_indices: ([int]) The list of indices which are valid targets for the next node
        :return: (int) The index of the next node
        """
        # Simple greedy algorithm.
        lowest_distance = 999.9
        lowest_distance_index = -1
        for index in target_address_indices:
            if self.all_distances[current_address_index][index] < lowest_distance:
                lowest_distance = self.all_distances[current_address_index][index]
                lowest_distance_index = index
        return lowest_distance_index

