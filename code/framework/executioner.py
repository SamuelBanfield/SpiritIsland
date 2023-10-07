import json


def main():
    with open('../../debug_controls.json', 'r') as json_file:
        debug_controls = json.load(json_file)
    # Make the start menu with options like picking your spirit
    if debug_controls["skip_menu"]:
        launch_game()
    else:
        # Do menu things
        launch_game()


def launch_game():
    # Create the UI and initalise the board, turn manager, and player state
    print('done')
    return


if __name__ == "__main__":
    main()
