# Jesse Perkins 001250868
from model.facility import Facility
from user_interface import UserInterface


def main():
    """*main*
        Create a facility object which has all package and distance data loaded, fix the bad
        address package, preload special packages, then load the remaining packages based on
        the nearest neighbor algorithm. After loading, run the package delivery routine.

        TIME: O(f(x)) = n^2

        SPACE: O(f(x))= n^2

    :return: None
    """
    facility = Facility()
    # Manually reassign the wrong package to have the correct information
    wrong_address_package = facility.all_packages.lookup(9)
    wrong_address_package.address = "410 S State St"
    wrong_address_package.city = "Salt Lake City"
    wrong_address_package.zipcode = 84111
    facility.all_packages.remove(9)
    facility.all_packages.insert(wrong_address_package.package_id, wrong_address_package)
    # Preload the packages into trucks
    facility.preload()
    package_list = facility.unassigned_packages
    # Assign remaining packages to trucks
    package_list = facility.loader(facility.all_trucks[2], package_list)
    package_list = facility.loader(facility.all_trucks[0], package_list)
    facility.loader(facility.all_trucks[1], package_list)
    # Deliver packages and modify the start time of the 2nd truck so that it
    # only leaves the facility after another truck returns
    facility.delivery(facility.all_trucks[0])
    facility.delivery(facility.all_trucks[2])
    if facility.all_trucks[0].current_time < facility.all_trucks[2].current_time:
        facility.all_trucks[1].current_time = facility.all_trucks[0].current_time
        facility.all_trucks[1].departure_time = facility.all_trucks[0].current_time
    else:
        facility.all_trucks[1].current_time = facility.all_trucks[2].current_time
        facility.all_trucks[1].departure_time = facility.all_trucks[2].current_time
    facility.delivery(facility.all_trucks[1])
    # Run the UI
    UserInterface.menu(facility)


if __name__ == "__main__":
    main()
