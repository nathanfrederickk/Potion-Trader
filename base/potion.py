class Potion:
    HASH_BASE = 27183

    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        """
        Constructor
        
        :param potion_type: type of potion
        :param name: potion name
        :param buy_price: buy price of potion
        :param quantity: quantity of potion
        :complexity: O(1)
        """
        self.potion_type = potion_type
        self.name = name
        if buy_price <= 0:
            raise ValueError("buy_price must be a positive number")
        else:
            self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """
        Creates a potion with quantity 0
        
        :param potion_type: name of the potion
        :param name: name of the potion
        :param buy_price: buy price of the potion
        :return: potion with quantity 0
        :complexity: O(1)
        """
        return Potion(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        Uniform Hash function. Takes into account all characters. Uses varying coefficients for all characters.

        :param potion_name: name of the potion
        :param tablesize: size of the Hash Table
        :return: unique key
        :complexity: O(N), where N is the length of string
        """
        value = 0
        for char in potion_name:
            value = (value * Potion.HASH_BASE + ord(char)) % tablesize
        return value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        Simple hash function. Returns the ASCII code of the first character modulo table size.
        
        :param potion_name: name of the potion
        :param tablesize: size of the Hash Table
        :return: a bad hash
        :complexity: O(1)
        """
        return ord(potion_name[0]) % tablesize
    
    def __str__(self) -> str:
        """
        Returns the name of potion, buy price and quantity.
        :complexity: O(1)
        """
        return '<type: ' + self.potion_type + ', name: ' + self.name + ', price: ' + str(self.buy_price) + ', quantity: ' + str(self.quantity) + '>'
