import datetime


class Package:
    """A class used to represent a package.

    **Instance Attributes**
        *package_id* (int):
            The unique package id, used to identify the package
        *address* (str):
            The package street address
        *city* (str):
            The city the street address is located in
        *zipcode* (int):
            The zipcode of the city
        *deadline: TimeClock
            The last acceptable package arrival time
        *weight* (float):
            The weight of the package in kg
        *note: str
            A note with special instructions regarding the package
        *delivery_status* (bool, optional):
            Whether the package has been delivered or not. The default is false for undelivered
        *delivery_time_stamp* (TimeClock):
            The time that the package was delivered.

    **Methods**
        *__init__* (package_id (int), address (str), city (str), zipcode (int), deadline (TimeClock), weight (float),
        note (str), delivery_status (bool, optional), delivery_time_stamp (TimeClock, optional) -> (None)
            - TIME: O(f(x)) = 1
            - SPACE: O(f(x))= 1
    """

    def __init__(self,  package_id: int, address: str, city: str, zipcode: int, deadline: datetime.datetime,
                 weight: float, note: str, delivery_status=False,
                 delivery_time_stamp=datetime.datetime.now().replace(hour=0, minute=0, second=0)) -> None:
        """__init__:
            Creates a Package object that contains all the information entered in.

            TIME: O(f(x)) = 1

            SPACE: O(f(x))= 1

        :param package_id: (int) The unique package ID
        :param address: (str) The street address of the package
        :param city: (str) The city in which the street address is located
        :param zipcode: (int) The zipcode of the street address / city combo
        :param deadline: (TimeClock) The time of day by which the package must arrive
        :param weight: (float) The weight of the package in kilograms
        :param note: (str) A note regarding the package and/or its delivery
        :param delivery_status: (bool, optional) Whether or not the package has been delivered (False for undelivered)
        :param delivery_time_stamp: (TimeClock, optional): what time the package was delivered
        :return: (None)
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.delivery_status = delivery_status
        self.delivery_time_stamp = delivery_time_stamp
    #
    # def get_package_details(self):
    #     package_details = f"\nPackage ID: {self.package_id}\n" \
    #                       f"Address: {self.address}\n" \
    #                       f"City: {self.city}\n" \
    #                       f"Zip Code: {self.zipcode}\n" \
    #                       f"Deadline: {self.deadline.hour}:{self.deadline.minute}\n" \
    #                       f"Weight: {self.weight}\n" \
    #                       f"Note: {self.note}\n" \
    #                       f"Status: {self.delivery_status}\n" \
    #                       f"Time of Delivery: {self.delivery_time_stamp.hour}:{self.delivery_time_stamp.minute}\n"
    #     return package_details
