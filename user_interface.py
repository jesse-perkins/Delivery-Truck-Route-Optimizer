from model.facility import Facility
from model.package import Package
import datetime


class UserInterface:
    """A class used to represent a Shipping Facility

    **Class Attributes**
        *MAIN_UI_COMMAND_LIST* ([str]):
            The list of acceptable commands.

    **Methods**
        *menu* (facility (Facility)) -> (None):
            - TIME: O(f(x))= n
            - SPACE: O(f(x))=
        *print_ui* (None) -> (None):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
        *is_integer* (string (str)) -> (bool):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
        *datetime_to_string* (package_datetime (datetime)) -> (str):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
        *string_to_datetime* (string_time (str)) -> (datetime or None):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
        *display_package_data* (display_package (Package or None)) -> (bool):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
        *display_package_data_condensed* (display_package (Package or None)) -> (bool):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
        *display_package_status* (display_package (Package or None), specified_time (datetime), left_hub (bool)) -> (bool):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
        *display_package_status_condensed* (display_package (Package or None), specified_time (datetime), left_hub (bool)) -> (bool):
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))=
    """

    MAIN_UI_COMMAND_LIST = ['l', 's', 'd', 'a', 'i', 'm', 'q', '']

    @staticmethod
    def menu(facility: Facility) -> None:
        """*menu*
            Displays and manages user input to display package and truck information

            TIME: O(f(x))= n

            SPACE: O(f(x))=

        :param facility: (Facility) The facility from which all data is pulled
        :return: (None)
        """
        command = ""
        while command != 'q':
            UserInterface.print_ui()
            command = input("-> ").lower()
            if len(command) > 1 or command not in UserInterface.MAIN_UI_COMMAND_LIST:
                print("Invalid entry, please enter a valid selection. Press enter to continue.")
                command = ""
                input("")

            elif command == UserInterface.MAIN_UI_COMMAND_LIST[0]:
                while command != 'm':
                    if not UserInterface.is_integer(command):
                        command = input("Please enter a package ID, or 'M' to return to the (M)ain menu -> ").lower()
                    else:
                        package_id = int(command)
                        found_package = None
                        for truck in facility.all_trucks:
                            if truck.package_list.lookup(package_id) is not None:
                                found_package = truck.package_list.lookup(package_id)
                                command = ''
                                break
                        print("\n\n")
                        if not UserInterface.display_package_data(found_package):
                            command = input("INVALID PACKAGE ID.\n"
                                            "Please enter a valid package ID,"
                                            "or enter 'M' to return to the (M)ain menu -> ").lower()
                        else:
                            print("\n")
                print("\n\n\n\n\n\n\n\n")
            elif command == UserInterface.MAIN_UI_COMMAND_LIST[1]:
                parsed_time = None
                while command != 'm':
                    if parsed_time is None:
                        command = input(
                            "\nPlease enter a specific time in the following format: HH:mm AM/PM -> ").lower()
                        parsed_time = UserInterface.string_to_datetime(command)
                    else:
                        command = ''
                        while command != 'm':
                            if not UserInterface.is_integer(command):
                                command = input(
                                    "\nPlease enter a package ID, or 'M' to return to the (M)ain menu -> ").lower()
                            else:
                                package_id = int(command)
                                found_package = None
                                has_left_hub = False
                                for truck in facility.all_trucks:
                                    if truck.package_list.lookup(package_id) is not None:
                                        found_package = truck.package_list.lookup(package_id)
                                        if truck.departure_time < parsed_time:
                                            has_left_hub = True
                                        command = ''
                                        break
                                if not UserInterface.display_package_status(found_package, parsed_time, has_left_hub):
                                    command = input("\nINVALID PACKAGE ID.\n"
                                                    "Please enter a valid package ID,"
                                                    "or enter 'M' to return to the (M)ain menu -> ").lower()
                print("\n\n\n\n\n\n\n\n")

            elif command == UserInterface.MAIN_UI_COMMAND_LIST[2]:
                sorted_package_list = [None] * 41
                for truck in facility.all_trucks:
                    for truck_package in truck.package_list.get_values():
                        sorted_package_list[truck_package.package_id] = truck_package
                print(
                    f"===================================================================================================================\n"
                    f"||                                              Package Information                                              ||\n"
                    f"===================================================================================================================")
                print(
                    " ID | ADDRESS                                | CITY             |ZIPCODE| DEADLINE   | KG    | NOTE")
                print(
                    "----|----------------------------------------|------------------|-------|------------|-------|---------------------")
                for sorted_package in sorted_package_list:
                    UserInterface.display_package_data_condensed(sorted_package)
                input("\n\nPress enter to continue.")
                command = 'm'
                print("\n\n\n\n\n\n\n\n")

            elif command == UserInterface.MAIN_UI_COMMAND_LIST[3]:
                parsed_time = None
                while command != 'm':
                    if parsed_time is None:
                        command = input(
                            "\nPlease enter a specific time in the following format: HH:mm AM/PM -> ").lower()
                        parsed_time = UserInterface.string_to_datetime(command)
                    else:
                        truck_count = 0
                        for truck in facility.all_trucks:
                            sorted_package_list = [None] * 41
                            truck_count += 1
                            has_left_hub = False
                            if truck.departure_time < parsed_time:
                                has_left_hub = True
                            print(f"\n====================================================\n"
                                  f"||         Package Status Data: Truck #{truck_count}          ||\n"
                                  f"====================================================")
                            print("ID | DEADLINE   | STATUS     | DELIVERY TIME\n"
                                  "---|------------|------------|----------------------")
                            for truck_package in truck.package_list.get_values():
                                sorted_package_list[truck_package.package_id] = truck_package
                            for current_package in sorted_package_list:
                                UserInterface.display_package_status_condensed(current_package, parsed_time, has_left_hub)

                        input("\n\nPress enter to continue.")
                        command = 'm'
                        break
                print("\n\n\n\n\n\n\n\n")
            elif command == UserInterface.MAIN_UI_COMMAND_LIST[4]:
                total_mileage = 0
                truck_number = 0
                print("\n\n")
                for truck in facility.all_trucks:
                    truck_number += 1
                    total_mileage += truck.miles_traveled
                    print(f"Truck {truck_number} traveled {round(truck.miles_traveled, 2)} miles")
                print(f"TOTAL MILES TRAVELED BY ALL TRUCKS: {round(total_mileage, 2)}")
                input("\n\nPress enter to continue.")
                command = 'm'
                print("\n\n\n\n\n\n\n\n")

    @staticmethod
    def print_ui():
        """*print_ui*
            Prints the user interface menu to terminal.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :return: None
        """
        print("\n\n===========================================\n"
              "=== WELCOME TO THE WGUPS PACKAGE ROUTER ===\n"
              "===========================================\n"
              "PLEASE SELECT ONE OF THE FOLLOWING: \n"
              "  L - (L)ookup package info by package ID\n"
              "  S - Lookup package (S)tatus by package ID\n"
              "  D - (D)isplay all package info\n"
              "  A - Display (A)ll package statuses\n"
              "  I - Display truck m[I]leage values\n"
              "  Q - (Q)uit application\n"
              )

    @staticmethod
    def is_integer(string: str) -> bool:
        """*is_integer*
            Determines whether or not a string value is an integer.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :param string: (str) The string to be checked
        :return: (bool) True for integer, False otherwise
        """
        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def datetime_to_string(package_datetime: datetime) -> str:
        """*datetime_to_string*
            Converts a datetime object into a formatted string.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :param package_datetime: (datetime) The datetime object to be converted into a formatted string
        :return: (str) The resultant formatted string
        """
        minutes = ''
        if package_datetime.minute < 10:
            minutes += '0'
        minutes += str(package_datetime.minute)
        hours = ''
        am_or_pm = "AM"
        if package_datetime.hour == 0:
            hours = '12'
        elif package_datetime.hour >= 12:
            am_or_pm = "PM"
            if package_datetime.hour >= 13:
                hours = str(package_datetime.hour - 12)
        if hours == '':
            hours = str(package_datetime.hour)
        time = f"{hours}:{minutes} {am_or_pm}"
        if hours == "11" and minutes == "59" and am_or_pm == "PM":
            time = "End of Day"
        return time

    # noinspection PyBroadException
    @staticmethod
    def string_to_datetime(string_time: str) -> datetime or None:
        """*datetime_to_string*
            Converts a formatted string into a datetime object.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :param string_time: (str) The string to be converted into a datetime object
        :return: (datetime or None) The resultant datetime object, or None if the string was not formatted properly.
        """
        try:
            first_split = string_time.split(':')
            second_split = first_split[1].split()
            hours = int(first_split[0])
            minutes = int(second_split[0])
            am_or_pm = second_split[1].lower()
            if am_or_pm != 'am' and am_or_pm != 'pm':
                raise Exception
            if am_or_pm.lower() == 'pm' and hours != 12:
                hours += 12
            return datetime.datetime.now().replace(hour=hours, minute=minutes, second=0)
        except Exception:
            return None

    @staticmethod
    def display_package_data(display_package: Package or None) -> bool:
        """*display_package_data*
            Prints a package's details to the console.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :param display_package: (Package) The package to be displayed
        :return: (bool) False if the input is None, otherwise true.
        """
        if display_package is None:
            return False
        else:
            time = UserInterface.datetime_to_string(display_package.deadline)
            print(f"Package ID: {display_package.package_id}\n"
                  f"Address: {display_package.address}\n"
                  f"City: {display_package.city}\n"
                  f"Zip Code: {display_package.zipcode}\n"
                  f"Deadline: {time}\n"
                  f"Weight: {display_package.weight}\n"
                  f"Note: {display_package.note}"
                  )
            return True

    @staticmethod
    def display_package_data_condensed(display_package: Package or None) -> bool:
        """*display_package_data_condensed*
            Prints a package's details to the console in a condensed format.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :param display_package: (Package) The package to be displayed
        :return: (bool) False if the input is None, otherwise true.
        """
        if display_package is None:
            return False
        else:
            time = UserInterface.datetime_to_string(display_package.deadline)
            print('{0:{width}}'.format(display_package.package_id, width=3), end=' | ')
            print('{0:{width}}'.format(display_package.address, width=38), end=' | ')
            print('{0:{width}}'.format(display_package.city, width=16), end=' | ')
            print('{0:{width}}'.format(display_package.zipcode, width=5), end=' | ')
            print('{0:{width}}'.format(time, width=10), end=' | ')
            print('{0:{width}}'.format(display_package.weight, width=5), end=' | ')
            print(display_package.note)
            return True

    @staticmethod
    def display_package_status(display_package: Package or None, specified_time: datetime, left_hub: bool) -> bool:
        """*display_package_status*
            Prints a package's status to the console based on the time of day and whether or not the truck has left
            the hub yet.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :param display_package: (Package) The package to be displayed
        :param specified_time: (datetime) The specific time to check the status for
        :param left_hub: (bool) Whether or not the truck has left the hub
        :return: (bool) False if the input is None, otherwise true.
        """
        if display_package is None:
            return False
        else:
            delivery_time = "Package not delivered"
            package_status = "At the Hub"
            if left_hub:
                if specified_time < display_package.delivery_time_stamp:
                    package_status = "En Route"
                else:
                    package_status = "Delivered"
                    delivery_time = UserInterface.datetime_to_string(display_package.delivery_time_stamp)
            print(f"\n\nPackage ID: {display_package.package_id}\n"
                  f"Deadline: {UserInterface.datetime_to_string(display_package.deadline)}\n"
                  f"Status: {package_status}\n"
                  f"Delivery Time: {delivery_time}"
                  )
            return True

    @staticmethod
    def display_package_status_condensed(display_package: Package or None, specified_time: datetime, left_hub: bool) -> bool:
        """*display_package_status_condensed*
            Prints a package's status to the console in a condensed format based on the time of day and whether or not
            the truck has left the hub yet.

            TIME: O(f(x))= 1

            SPACE: O(f(x))=

        :param display_package: (Package) The package to be displayed
        :param specified_time: (datetime) The specific time to check the status for
        :param left_hub: (bool) Whether or not the truck has left the hub
        :return: (bool) False if the input is None, otherwise true.
        """
        if display_package is None:
            return False
        else:
            delivery_time = "Package not delivered"
            package_status = "At the Hub"
            if left_hub:
                if specified_time < display_package.delivery_time_stamp:
                    package_status = "En Route"
                else:
                    package_status = "Delivered"
                    delivery_time = UserInterface.datetime_to_string(display_package.delivery_time_stamp)
            if UserInterface.datetime_to_string(display_package.deadline) == "E.O.D":
                print('{0:{width}}'.format(display_package.package_id, width=4), end=' | ')
                print('{0:{width}}'.format(UserInterface.datetime_to_string(display_package.deadline), width=10), end=' | ')
                print('{0:{width}}'.format(package_status, width=10), end=' | ')
                print(delivery_time)
            else:
                print('{0:{width}}'.format(display_package.package_id, width=2), end=' | ')
                print('{0:{width}}'.format(UserInterface.datetime_to_string(display_package.deadline), width=10), end=' | ')
                print('{0:{width}}'.format(package_status, width=10), end=' | ')
                print(delivery_time)
            return True
