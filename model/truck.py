from dataStructures.hashtable import HashTable
import datetime


class Truck:
    """A class used to represent a delivery truck.

    **Class Attributes**
        *MILES_PER_HOUR* (int):
            The miles traveled per hour of travel time.
        *DEPARTURE_TIME* (TimeClock):
            The default time the truck left the hub.
        *MAX_PACKAGES* (int):
            The max number of packages in a vehicle.

    **Instance Attributes**
        *current_time* (TimeClock):
            The current time on the truck, to be used for calculating package times.
        *package_list* (HashTable):
            The packages on the truck.
        *miles_traveled* (float):
            The number of miles traveled by the truck.

    **Methods**
        *__init__* (departure_time (TimeClock, optional), number_of_packages (int, optional)) -> None
            - TIME: O(f(x))= n
            - SPACE: O(f(x))= n
    """
    MILES_PER_HOUR: int = 18
    DEPARTURE_TIME: datetime.datetime = datetime.datetime.now().replace(hour=8, minute=0, second=0)
    MAX_PACKAGES: int = 16

    def __init__(self, departure_time: datetime = DEPARTURE_TIME, number_of_packages: int = MAX_PACKAGES) -> None:
        """*__init__*
            Creates a truck with the supplied departure time and package load capacity.

            TIME: O(f(x))= n

            SPACE: O(f(x))= n

        :param departure_time: (TimeClock, optional) the time the truck leaves the depot
        :param number_of_packages: (int, optional) the number of packages the truck will carry, capped at MAX_PACKAGES
        :return: (None)
        """
        if number_of_packages > Truck.MAX_PACKAGES:
            number_of_packages = Truck.MAX_PACKAGES
        self.package_list: HashTable = HashTable(number_of_packages * 2)
        self.current_time: datetime.datetime = departure_time
        self.departure_time: datetime.datetime = departure_time
        self.miles_traveled: float = 0.0
