from typing import Generator


def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed


class RandomGen:

    def __init__(self, seed: int = 0) -> None:
        """
        Constructor for RandomGen
        
        :param seed: an integer
        :complexity: O(1)
        """
        self.seed = seed
        self.generated_numbers = lcg(pow(2, 32), 134775813, 1, self.seed)

    def randint(self, k: int) -> int:
        """
        Generates a random number from 1 to k inclusive

        Example:
            
            When k is 4,
            There will be 5 numbers generated:
                1
                134775814
                3698175007
                870078620
                1172187917

            Which in binary would be equivalent to:
                00000000000000000000000000000001
                00001000000010001000010000000110
                11011100011011011010110000011111
                00110011110111000101100010011100
                01000101110111100010101100001101

            And after dropping the last 16 bits, it will be:
                0000000000000000
                0000100000001000
                1101110001101101
                0011001111011100
                0100010111011110

            By comparing each bit in each position if it is a 1 and if 3 or more of those 5 numbers have a 1 in that
            position, the final number would be:
                0000000001001100, which is equivalent to 76

            And after performing the modulus operation with k and incrementing it,
                (76 % 4) + 1 = 1

            Hence, the returned number would be 1.
            This method will keep taking the next 5 numbers no matter the amount of times it has been called
        
        :param k: range of which the number is generated
        :return: random number
        :complexity: O(1)
        """
        if k == 0:
            raise ValueError("k can only be greater or equal to 1")

        random_num = [next(self.generated_numbers) for _ in range(5)]
        binary = []  # len = 5
        for num in random_num:  # O(1), only runs 5 times
            binary.append('{0:032b}'.format(num)[:16])  # generate a 32 bit number and drop 16 bits

        res = ''
        for bit in range(16):       # O(1)
            count = 0
            for n in binary:        # O(1), because binary is a list of length 5
                if n[bit] == '1':   # counter for how many numbers have 1 in the current bit
                    count += 1
            if count >= 3:          # checks if 3 or more the 5 numbers if the current bit is a 1
                res += '1'          # places a "1" in that current position in the new number
            else:
                res += '0'          # otherwise, place a "0" in the new number
        return int(res, 2) % k + 1  # O(1)
    

if __name__ == "__main__":
    Random_gen = lcg(pow(2, 32), 134775813, 1, 0)
