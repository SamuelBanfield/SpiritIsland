import json
import sys
from pathlib import Path


def read_json(filepath: str) -> dict:
    """
    Reads a json file into a dict
    :param filepath: path to json file
    :return: dictionary of json file contents
    """
    with open(Path(filepath), "r") as file:
        json_dict = json.load(file)
    return json_dict


class Runner:
    """Class for running the game"""

    def __init__(self, controls_path: str):
        """
        Initialise.
        :param controls_path: path to debug_controls file
        """
        self.controls = read_json(controls_path)

        print('Runner initialised')

    def do_stuff(self):
        print('stuff done')
        return


def main():
    """Main function - run Spirit Island"""
    # Path to debug controls
    controls_path = '../debug_controls.json'

    # Create the runner
    runner = Runner(controls_path)
    runner.do_stuff()

    print('breakpoint')


if __name__ == "__main__":
    main()
