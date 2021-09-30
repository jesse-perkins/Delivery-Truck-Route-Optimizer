class HashTable:
    """A class used to store data. This is a chaining HashTable, so the lookup and remove functions have a worst case
    O(f()) = n. This case only occurs when all items are inserted into the same slot on the HashMap. While technically
    possible, it is a bit contrived.

    **Instance Attributes**
        *table* ( [[(int, object)]] ):
            The foundation of the HashTable. It is a list of lists of key / value pairs.

    **Methods**
        *__init__* (table_size (int, optional)) -> None
            - TIME: O(f(x))= n
            - SPACE: O(f(x))= n
        *insert* (key (int), value (object)) -> None
            - TIME: O(f(x))= 1
            - SPACE: O(f(x))= 1
        *remove* (key (int)) -> bool:
            - TIME: Best: O(f(x))= 1
            - TIME: Worst: O(f(x))= n
            - SPACE: O(f(x))= 1
        *lookup* (key (int)) -> object:
            - TIME: Best: O(f(x))= 1
            - TIME: Worst: O(f(x))= n
            - SPACE: O(f(x))= 1
        *get_keys* () -> [int]:
            - TIME: O(f(x))= n
            - SPACE: O(f(x))= n
        *get_values* () -> [object]:
            - TIME: O(f(x))= n
            - SPACE: O(f(x))= n
    """
    def __init__(self, table_size=10) -> None:
        """__init__:
            Creates the initial empty HashTable. The default size is 10.

            TIME: O(f(x))= n

            SPACE: O(f(x))= 1

        :param table_size: (int, optional) The number of slots in the initial HashTable
        :return: None
        """
        self.item_count = 0
        row_count = 0
        self.table = []
        while row_count < table_size:
            self.table.insert(row_count, [])
            row_count += 1

    def insert(self, key: int, value: object) -> None:
        """insert:
            Inserts an entry into the HashTable. If an item happens to hash into the same slot, it is added to the end.

            TIME: O(f(x))= 1

            SPACE: O(f(x))= 1

        :param key: (int) The key for the lookup of the value
        :param value: (object) The object to be stored in the HashTable
        :return: None.
        """
        hashed_key = hash(key) % len(self.table)
        self.table[hashed_key].append((key, value))
        self.item_count += 1

    def remove(self, key: int) -> bool:
        """remove:
            Removes the value with the specified key from the HashTable.

            TIME:
                - Best: O(f(x))= 1
                - Worst: O(f(x))= n

            SPACE: O(f(x))= 1

        :param key: (int) The key of the value to be removed
        :return: (bool) Whether or not the value was found and removed
        """
        hashed_key = hash(key) % len(self.table)
        for key_value_pair in self.table[hashed_key]:
            if key_value_pair[0] == key:
                self.table[hashed_key].remove(key_value_pair)
                self.item_count -= 1
                return True
        return False

    def lookup(self, key: int) -> object:
        """lookup:
            Searches for an item and returns that item.

            TIME:
                - Best: O(f(x))= 1
                - Worst: O(f(x))= n

            SPACE: O(f(x))= 1

        :param key: (int) The key of the value to be looked up
        :return: (object) The object returned by the lookup, None if the object is not found
        """
        hashed_key = hash(key) % len(self.table)
        for key_value_pair in self.table[hashed_key]:
            if key_value_pair[0] == key:
                return key_value_pair[1]
        return None

    def get_keys(self) -> [int]:
        """get_keys:
            Gathers and returns all object keys in a list.

            TIME: O(f(x))= n

            SPACE: O(f(x))= n

        :return: ([int]) The list of all keys stored in the HashTable
        """
        all_keys = []
        for row in self.table:
            for item in row:
                all_keys.append(item[0])
        return all_keys

    def get_values(self) -> [object]:
        """get_values(self) -> [object]:
            Gathers and returns all objects in a list.

            TIME: O(f(x))= n

            SPACE: O(f(x))= n

        :return: ([object]) The list of all value objects stored in the HashTable
        """
        all_values = []
        for row in self.table:
            for item in row:
                all_values.append(item[1])
        return all_values
