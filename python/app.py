import random
import unittest


class Dice:
    def __init__(self, number_of_dice):
        """
        Initialize a Dice object that can roll N dice.
        
        Args:
            number_of_dice: The number of dice to roll
        """
        self.number_of_dice = number_of_dice
    
    def toss_and_sum(self):
        """
        Roll all N dice and return the sum of their values.
        
        Returns:
            The sum of all dice rolls (each die is 1-6)
        """
        total = sum(random.randint(1, 6) for _ in range(self.number_of_dice))
        return total


class Bins:
    def __init__(self, min_value, max_value):
        """
        Initialize a Bins tracking object for a range of values.
        
        Args:
            min_value: The minimum bin value (inclusive)
            max_value: The maximum bin value (inclusive)
        """
        self.min_value = min_value
        self.max_value = max_value
        # Initialize bins dictionary with all values in range set to 0
        self.bins = {i: 0 for i in range(min_value, max_value + 1)}
    
    def increment_bin(self, value):
        """
        Increment the count for a specific bin value.
        
        Args:
            value: The bin value to increment
        
        Raises:
            ValueError: If value is outside the valid range
        """
        if value not in self.bins:
            raise ValueError(f"Value {value} is outside the range [{self.min_value}, {self.max_value}]")
        self.bins[value] += 1
    
    def get_bin(self, value):
        """
        Get the count for a specific bin value.
        
        Args:
            value: The bin value to retrieve
        
        Returns:
            The count for the specified bin
        
        Raises:
            ValueError: If value is outside the valid range
        """
        if value not in self.bins:
            raise ValueError(f"Value {value} is outside the range [{self.min_value}, {self.max_value}]")
        return self.bins[value]


class Simulation:
    def __init__(self, numberOfDies, numberOfTosses):
        """
        Initialize a Simulation object.
        
        Args:
            numberOfDies: The number of dice to throw per toss
            numberOfTosses: The number of times to toss the dice
        """
        self.numberOfDies = numberOfDies
        self.numberOfTosses = numberOfTosses
        self.dice = Dice(numberOfDies)
        # Calculate the minimum and maximum possible sums
        # Minimum: numberOfDies * 1, Maximum: numberOfDies * 6
        self.min_sum = numberOfDies
        self.max_sum = numberOfDies * 6
        self.results = Bins(self.min_sum, self.max_sum)
    
    def run_simulation(self):
        """Run the simulation: toss dice numberOfTosses times and track results."""
        for _ in range(self.numberOfTosses):
            toss_sum = self.dice.toss_and_sum()
            self.results.increment_bin(toss_sum)
    
    def print_results(self):
        """Print the simulation results in a formatted table with histogram."""
        print("***")
        print(f"Simulation of {self.numberOfDies} dice tossed for {self.numberOfTosses} times.")
        print("***")
        print()
        
        for sum_value in range(self.min_sum, self.max_sum + 1):
            count = self.results.get_bin(sum_value)
            percentage = count / self.numberOfTosses
            # Create histogram bar: asterisks = floor(percentage * 100)
            histogram_bars = int((count / self.numberOfTosses) * 100)
            
            print(f"{sum_value:2d} : {count:8d}: {percentage:.2f} {'*' * histogram_bars}")


if __name__ == '__main__':
    sim = Simulation(2, 1000000)
    sim.run_simulation()
    sim.print_results()


class TestDice(unittest.TestCase):
    
    def test_dice_sum_in_valid_range(self):
        """Test that the sum of N dice rolls is within valid range"""
        dice = Dice(2)
        # For 2 dice, minimum is 2 (1+1) and maximum is 12 (6+6)
        for _ in range(100):
            result = dice.toss_and_sum()
            self.assertGreaterEqual(result, 2)
            self.assertLessEqual(result, 12)
    
    def test_single_die_range(self):
        """Test that a single die roll is between 1 and 6"""
        dice = Dice(1)
        for _ in range(100):
            result = dice.toss_and_sum()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)
    
    def test_five_dice_range(self):
        """Test that 5 dice rolls produce sum between 5 and 30"""
        dice = Dice(5)
        # For 5 dice, minimum is 5 (1+1+1+1+1) and maximum is 30 (6+6+6+6+6)
        for _ in range(100):
            result = dice.toss_and_sum()
            self.assertGreaterEqual(result, 5)
            self.assertLessEqual(result, 30)
    
    def test_dice_rolls_produce_variance(self):
        """Test that multiple rolls produce different values (randomness)"""
        dice = Dice(2)
        rolls = [dice.toss_and_sum() for _ in range(20)]
        # It's extremely unlikely that all 20 rolls produce the same value
        self.assertGreater(len(set(rolls)), 1)


class TestBins(unittest.TestCase):
    
    def test_bins_initialization(self):
        """Test that bins are properly initialized with zero counts"""
        bins = Bins(2, 12)
        # All bins should start at 0
        for value in range(2, 13):
            self.assertEqual(bins.get_bin(value), 0)
    
    def test_increment_bin(self):
        """Test that incrementing a bin increases its count"""
        bins = Bins(2, 12)
        bins.increment_bin(7)
        self.assertEqual(bins.get_bin(7), 1)
        bins.increment_bin(7)
        self.assertEqual(bins.get_bin(7), 2)
    
    def test_multiple_bins(self):
        """Test that incrementing one bin doesn't affect others"""
        bins = Bins(2, 12)
        bins.increment_bin(2)
        bins.increment_bin(7)
        bins.increment_bin(12)
        self.assertEqual(bins.get_bin(2), 1)
        self.assertEqual(bins.get_bin(7), 1)
        self.assertEqual(bins.get_bin(12), 1)
        self.assertEqual(bins.get_bin(6), 0)
    
    def test_invalid_bin_value(self):
        """Test that accessing bins outside range raises ValueError"""
        bins = Bins(2, 12)
        with self.assertRaises(ValueError):
            bins.increment_bin(1)
        with self.assertRaises(ValueError):
            bins.get_bin(13)


if __name__ == '__main__':
    unittest.main()

