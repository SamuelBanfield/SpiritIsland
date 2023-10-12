import unittest
from spirit_island import launcher

class TestAdjacencies(unittest.TestCase):

    def test_board_d(self):
        board_d = launcher.read_json("./spirit_island/resources/board_d_coords.json")
        polygons = {}
        for key in board_d.keys():
            polygons[key] = [tuple(coord) for coord in board_d[key]["polygon"]]
        expected_adjacencies = launcher.read_json("./spirit_island/resources/board_adjacencies.json")
        actual_adjacencies = {}
        for land in range(1, 9):
            for other_land in range(land + 1, 9):
                if len(set(polygons[str(land)]).intersection(set(polygons[str(other_land)]))) > 0:
                    if land in actual_adjacencies:
                        actual_adjacencies[land].append(other_land)
                    else:
                        actual_adjacencies[land] = [other_land]
                    if other_land in actual_adjacencies:
                        actual_adjacencies[other_land].append(land)
                    else:
                        actual_adjacencies[other_land] = [land]

        for land in expected_adjacencies:
            assert set(expected_adjacencies[land]) == set(actual_adjacencies[int(land)]), actual_adjacencies