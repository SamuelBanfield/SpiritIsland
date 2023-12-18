import unittest

from spirit_island.framework.elements import *


class TestElements(unittest.TestCase):

    def test_element_equality(self):
        one_air = ElementalThreshold({air: 1})
        two_air = ElementalThreshold({air: 2})
        one_animal = ElementalThreshold({animal: 1})
        two_air_one_animal = ElementalThreshold({air: 2, animal: 1})
        one_animal_two_air = ElementalThreshold({animal: 1, air: 2})

        def assert_elements_not_equal(first, second):
            assert (
                first != second
            ), f"{first} and {second} were unexpectedly equal"
            assert (
                hash(first) != hash(second)
            ), f"Hashes for {first} and {second} were unexpectedly equal"
        def assert_elements_equal(first, second):
            assert (
                first == second
            ), f"{first} and {second} were unexpectedly unequal"
            assert (
                hash(first) == hash(second)
            ), f"Hashes for {first} and {second} were unexpectedly unequal"

        assert_elements_not_equal(one_air, two_air)
        assert_elements_not_equal(one_air, one_animal)
        assert_elements_not_equal(one_air, two_air_one_animal)

        assert_elements_equal(one_animal_two_air, two_air_one_animal)

    def test_threshold_satisfies(self):
        one_animal_two_air = ElementalThreshold({animal: 1, air: 2})

        def assert_satisfies_threshold(elements, threshold):
            assert (
                threshold.is_satisfied_by(elements)
            ), f"Elements {elements} unexpectedly did not satisfy threshold {threshold}"
        def assert_does_not_satisfy_threshold(elements, threshold):
            assert (
                not threshold.is_satisfied_by(elements)
            ), f"Elements {elements} unexpectedly satisfied threshold {threshold}"

        assert_satisfies_threshold({animal: 1, air: 2}, one_animal_two_air)
        assert_satisfies_threshold({}, ElementalThreshold({}))
        assert_satisfies_threshold({animal: 2, air: 3, plant: 1}, one_animal_two_air)
        assert_does_not_satisfy_threshold({animal: 1, air: 1}, one_animal_two_air)
        assert_does_not_satisfy_threshold({animal: 1}, one_animal_two_air)
        assert_does_not_satisfy_threshold({}, one_animal_two_air)

        
            