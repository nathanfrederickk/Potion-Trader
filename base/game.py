"""
For this game class, we're using the hash table for the set_total_potion_data to store all potions with quantity/litre
0, using the potion_name as key and potion object as the item. A hash table is used because we are allowed to
assume that all hash operations take constant time. An AVL tree data structure is used in add_potions_to_inventory,
where the key is the the buy_price while the item contains the potion object. We choose the AVL tree data structure
here because we need to select the kth most expensive potion based on a random number generated in
choose_potions_for_vendors using the kth_largest() method in avl.py.
"""
from __future__ import annotations
# ^ In case you aren't on Python 3.10

from random_gen import RandomGen
from potion import Potion
from hash_table import LinearProbePotionTable
from avl import AVLTree


class Game:

    def __init__(self, seed=0) -> None:
        """
        Constructor for game
        
        :param seed: an integer
        :complexity: O(1)
        """
        self.rand = RandomGen(seed=seed)
        self.inventory_tree = AVLTree()
        self.potion_data_table = None
        self.hash_table_data = None  # Used in set_total_potion_data to create a copy for the potion_data for that day
        self.potion_name_amount_pairs_copy = None  # Used in add_potions_to_inventory to create copy of potion_name_amount_pairs

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        Sets the data of the potion that could possibly enter the vendor inventory
        over the course of the game (used hash table adt to store the data). The 3 values of the 
        list will be passed to Potion.create_empty that we created earlier. This method also set 
        the inventory of the vendors to contain 0 Litres of every potion listed.
        Example:
            
            potion_data[0] = 'Potion of Health Regeneration' and the hash value = 5
            potion_data[1] = 'Potion of Extreme Speed' and the hash value = 1
            potion_data[2] = 'Potion of Deadly Poison' and the hash value = 0
            potion_data[3] = 'Potion of Instant Health' and the hash value = 2
            potion_data[4] = 'Potion of Increased Stamina' and the hash value = 3
            potion_data[5] = 'Potion of Untenable Odour' and the hash value = 4
            
            then the hash table will look like:
                
                (Potion of Deadly Poison, <<potion.Potion object at SOME _ADDR>)
                (Potion of Extreme Speed,<potion.Potion object at SOME _ADDR>)
                (Potion of Instant Health,<potion.Potion object at SOME _ADDR>)
                (Potion of Increased Stamina,<potion.Potion object at SOME _ADDR>)
                (Potion of Untenable Odour,<potion.Potion object at SOME _ADDR>)
                (Potion of Health Regeneration,<potion.Potion object at SOME _ADDR>)
                
            ** to know what exactly is <potion.Potion object at SOME _ADDR>, I added a __str__()
               method in Potion class. So the final output of the data in hash table will be
               
               (Potion of Deadly Poison,<type: Damage, name: Potion of Deadly Poison, price: 45, quantity: 0>)
               (Potion of Extreme Speed,<type: Buff, name: Potion of Extreme Speed, price: 10, quantity: 0>)
               (Potion of Instant Health,<type: Health, name: Potion of Instant Health, price: 5, quantity: 0>)
               (Potion of Increased Stamina,<type: Buff, name: Potion of Increased Stamina, price: 25, quantity: 0>)
               (Potion of Untenable Odour,<type: Damage, name: Potion of Untenable Odour, price: 1, quantity: 0>)
               (Potion of Health Regeneration,<type: Health, name: Potion of Health Regeneration, price: 20, quantity: 0>)
                   
        :param potion_data: a list of list containing 3 element, which is the potion_name,
                            potion_type and buy_price
                            
        :complexity explanation:  𝐎(𝑁). The for loop takes O(N) times where N is the number of potions
                                  provided. The inside of the loop is constant because it is assigning
                                  and inserting an element to potion_data_table (hash table). This also takes
                                  constants time as we are allowed to assume that all hash table operations
                                  take constant time. To conclude, it's O(N)
        """
        self.hash_table_data = potion_data  # used in choose_potion, O(1)
        self.potion_data_table = LinearProbePotionTable(len(potion_data))
        for potion in potion_data:  # O(N)
            potion_name, potion_type, buy_price = potion[0], potion[1], potion[2]  # O(1)
            self.potion_data_table[potion_name] = Potion.create_empty(potion_type, potion_name, buy_price)  # O(1)

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Adds litres of particular potions into the current inventory of the vendor company
        Example:
            
            After adding quantity to the data in hash table:
                
                (Potion of Deadly Poison,<type: Damage, name: Potion of Deadly Poison, price: 45, quantity: 0>)
                (Potion of Extreme Speed,<type: Buff, name: Potion of Extreme Speed, price: 10, quantity: 5>)
                (Potion of Instant Health,<type: Health, name: Potion of Instant Health, price: 5, quantity: 3>)
                (Potion of Increased Stamina,<type: Buff, name: Potion of Increased Stamina, price: 25, quantity: 10>)
                (Potion of Untenable Odour,<type: Damage, name: Potion of Untenable Odour, price: 1, quantity: 5>)
                (Potion of Health Regeneration,<type: Health, name: Potion of Health Regeneration, price: 20, quantity: 4>)
                
            ** Notice the quantity is no longer as 0
            
            While adding the liters of particular potions into the hash table, we also create a tree where key: potion's buy_price,
            and item: Potion object. This is because we need to find the kth most expensive potion based on a random number generated.
            
            Thus, the AVL tree will look like:
                
                10
                ╟─5
                ║ ╟─1
                ║ ╙─
                ╙─20
                  ╟─
                  ╙─25
                
        :param potion_name_amount_pairs: a list of tuples containing two elements which is name of the
                                         potion and amount in litres
                                         
        :complexity explanation:  𝐎(𝐶 × log(𝑁)). The for loop takes O(C) time where C is the length of
                                  potion_name_amount_pairs. Inside the for loop, it is constant time when
                                  we get item from the potion_data_table (hash table) as we are allowed to
                                  assume that all hash table operations take constant time. It takes
                                  O(logN) when we insert an element to an AVL tree, where N is the number
                                  of potions provided in set_total_potion_data. To conclude, it's O(ClogN).
        """
        self.potion_name_amount_pairs_copy = potion_name_amount_pairs  # used in choose_potion, O(1)
        for potion_name, amount_of_liter in potion_name_amount_pairs:  # O(C)
            current_potion = self.potion_data_table[potion_name]  # current potion is a potion object, O(1)
            current_potion.quantity += amount_of_liter  # assign the empty potion to how many liters it contain, O(1)
            self.inventory_tree[current_potion.buy_price] = current_potion  # O(log(N))
     
    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Completes the vendor potion selection process and return a list, specifying what the vendors
        will sell. Each element in the list should be a tuple containing a string and a float, where
        the xth index contains the name of the potion that vendor x will sell, as well as the quantity
        of liters of that potion that was in inventory
        
        Example:
            
            original inventory tree:
                
                10
                ╟─5
                ║ ╟─1
                ║ ╙─
                ╙─20
                  ╟─
                  ╙─25
            
        1st loop,
            generated random number: 2 and we found that the key 20 is the 2nd largest in the tree, so we
            append the corresponding potion to the list and delete the node:
            potions_for_vendors = [('Potion of Health Regeneration', 4)]
            inventory_tree: 
                10
                ╟─5
                ║ ╟─1
                ║ ╙─
                ╙─25
                
        2nd loop,
        generated random number: 2 and we found that the key 10 is the 2nd largest in the tree, so we
        append the corresponding potion to the list and delete the node:
            potions_for_vendors = [('Potion of Health Regeneration', 4), ('Potion of Extreme Speed', 5)]
            inventory_tree: 
                5
                ╟─1
                ╙─25
                
        3rd loop,
        .
        .
        .
        
        len(num_vendor)th loop,
        
        once the loop ends, we need to insert back all the nodes that we have deleted and return the
        potions_for_vendors list.

        :param: num_vendors: s a single integer > 0, specifying how many vendors will sell potions.
        :return: a list of tuple
        
        :complexity explanation:  𝐎(𝐶 × log(𝑁)). The for loop takes O(C) time where C is equal to
                                  num_vendors. Inside the for loop we need to find the kth_largest
                                  node in the tree so that function takes O(logN), getting a random
                                  number takes O(logN), appending takes constant time, deleting a node
                                  from AVL tree take O(logN) where N is the number of potion provided
                                  in set_total_potion_data. After the for loop ends. We call the 
                                  set_total_potion_data method and add_potions_to_inventory method which 
                                  also takes O(ClogN). To conclude, it's O(ClogN + ClogN) which is equivalent to
                                  O(ClogN).
        """
        if num_vendors < 0:  # O(1)
            raise ValueError("num_vendors cannot be < 0")
            
        potions_for_vendors = []  # O(1)
        for _ in range(num_vendors):  # O(C)
            random_num = self.rand.randint(len(self.inventory_tree))  # # O(log(N))
            current_potion = self.inventory_tree.kth_largest(random_num).item  # O(log(N))
            potions_for_vendors.append((current_potion.name, current_potion.quantity))  # O(1)
            del self.inventory_tree[current_potion.buy_price]  # O(log(N))
        
        # insert the node back to the inventory tree in case the tree is been called again by the same object
        # we need to clear the tree before reinserting as the position of inserting matters the shape of the tree
        if self.inventory_tree.root:  # check if the tree has a root, O(1)
            self.inventory_tree.clear()  # O(1)
        self.set_total_potion_data(self.hash_table_data)  # restore the starting potion into the hash table called potion_data_table, O(N)
        self.add_potions_to_inventory(self.potion_name_amount_pairs_copy)  # add the elements(buy price) back to the inventory_tree, O(Clog(N))

        return potions_for_vendors  # O(1)

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[float]) -> list[float]:
        """
        Given a list od starting money for each day, compute the max profit earned.

        :param potion_valuations: a list of potions that each vendor is selling, paired with its
                                  valuation by the adventurers. (How much the adventurers will pay per
                                  litre for the potion).
        :param starting_money: list containing, for each attempt, the starting allowance the player has.
        :return: a list of single floating point number for each element of starting_money. The maximum money
                 that the player can have at the end of the day, given they start the day with the corresponding
                 entry in starting_money.
                 
        :complexity explanation:  𝐎(𝑁 × log(𝑁) + 𝑀 × 𝑁). The first for loops takes O(N) time where N is the length
                                  of potion_valuations. everything inside this for loop is constant because it is
                                  only assigning and comparing. Appending is also constant. Then we do the sorting
                                  where it takes O(NlogN) for merge sort. The second for loop (outer) takes O(M) 
                                  times where M is the length of starting money. Then the inner for loop of the 
                                  second for loop takes O(N) time and everything inside the inner for loop perform
                                  constant time because it is doing assigning, comparing and appending. So to sum it
                                  all up, it's O(N + NlogN + MN) which is equivalent to O(NlogN + MN).
                                  
        :text explanation: For solve_game, we first loop through the potion_valuations list and count the
                           profit_price_ratio (selling_price - buy_price) / buy_price. We append the profit_price_ratio
                           into a list named profits for later use. The list (profits) of tuple contains 3
                           elements (profit_ratio_price, potion_name, selling_price). Then we sort the elements in the
                           list using merge sort where the highest ratio is at the front. After sorting, we use a for
                           loop to loop through the starting_money with another nested loop to loop through the list
                           (profits) that we had created earlier. The inner loop is for us to access the potion that has
                           the largest profit that we would take for each day. Then we calculated how many liters we
                           could buy with a specific amount of money. If the result is greater than what the vendors
                           have, we will then take the maximum liters from the vendor, but if the result is lesser than
                           what the vendors have, we will take what we have counted. To calculate how much we can earn,
                           we multiplied the liters and selling price. After we bought the potion, we decrement our
                           money for that day with the liters multiplied by the buy_price. So when the money runs out,
                           we append what we have earned to another list called total_profits_per_day. But if the money
                           is insufficient to buy another potion, we will append what we have earned plus the remaining
                           money to the list(total_profits_per_day). Finally, when we reach the end of starting money,
                           we return the list (total_profits_per_day) which shows the maximum profit we can earn in each
                           day.
        """
        # total = O(Nlog(N) + MxN + N) = O(Nlog(N) + MxN)
        profits, total_profits_per_day = [], []  # O(1)
        if len(potion_valuations) == 0:  # if no potions to buy, O(1)
            return starting_money  # O(1)
        # O(N)
        for values in potion_valuations:  # O(N)
            current_potion = self.potion_data_table[values[0]]  # get the potion in hash table, O(1)
            profit = values[1] - current_potion.buy_price  # get the profit, O(1)
            if profit > 0 and current_potion.quantity > 0:  # O(1)
                profit_price_ratio = profit / current_potion.buy_price  # O(1)
                profits.append((-profit_price_ratio, values[0], values[1]))  # O(1), profits stores [(profit_price_ratio, potion_name, selling_price)]

        # O(Nlog(N))
        profits = self.merge_sort(profits)  # O(Nlog(N))
        
        # O(MxN)
        for money in starting_money:  # O(M)
            earn = 0  # O(1)
            for profit, potion_name, selling in profits:  # O(N)
                current_potion = self.potion_data_table[potion_name]  # get the current potion in hash table, O(1)
                liters = money / current_potion.buy_price  # O(1)
                if liters >= current_potion.quantity:  # O(1)
                    earn += current_potion.quantity * selling  # O(1)
                    money -= current_potion.buy_price * current_potion.quantity  # O(1)
                else:
                    earn += liters * selling  # O(1)
                    money -= current_potion.buy_price * liters  # O(1)
                if money == 0:  # O(1)
                    total_profits_per_day.append(earn)  # O(1)
                    break
            if money != 0:  # if we have money left but we can't buy anything due to lack of potions to buy, O(1)
                total_profits_per_day.append(earn + money)  # sum up what we earn and the money we left, O(1)
        return total_profits_per_day  # O(1)
        
    def merge_sort(self, array: list[tuple[float, str, float]]) -> list[tuple[float, str, float]]:
        """
        Recursive algorithm that divides input array into two halves, calls itself for the two halves and then merges
        the two sorted halves
        
        :param array: an array
        :return: a sorted array
        :complexity: O(NlogN)*CompEq, where n is the number of elements in the array and CompEq is the complexity of
                     the comparison
        """
        tmp = [None]*len(array)
        start = 0
        end = len(array) - 1
        self.__merge_sort_aux(array, start, end, tmp)
        return array

    def __merge_sort_aux(self, array: list[tuple[float, str, float]], start: int, end: int, tmp: list[None]) -> None:
        """
        Splits the array into two halves. Then it calls __merge_array to do the comparing and merging. Lastly copy
        everything from tmp to the original array.
        
        :param array: an array
        :param start: 0
        :param end: len(array) -1
        :param tmp: a temporary array to store the merged (partial) solution
        """
        if not start == end:
            mid = (start + end) // 2
            self.__merge_sort_aux(array, start, mid, tmp)
            self.__merge_sort_aux(array, mid+1, end, tmp)
            self.__merge_array(array, start, mid, end, tmp)
            for i in range(start, end+1):
                array[i] = tmp[i]

    def __merge_array(self, array: list[tuple[float, str, float]], start: int, mid: int, end: int, tmp: list[None]) -> None:
        """
        Compare and merge the array back.
        
        :param array: an array
        :param start: 0
        :param end: len(array) -1
        :param tmp: a temporary array to store the merged (partial) solution
        """
        ia = start
        ib = mid + 1
        for k in range(start, end+1):
            if ia > mid:
                tmp[k] = array[ib]
                ib += 1
            elif ib > end:
                tmp[k] = array[ia]
                ia += 1
            elif array[ia][0] <= array[ib][0]:
                tmp[k] = array[ia]
                ia += 1
            else:
                tmp[k] = array[ib]
                ib += 1