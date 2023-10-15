from spirit_island import launcher
from spirit_island.framework.island import Island
from spirit_island.ui.ui import UI

if __name__ == "__main__":
    """To run from console"""
    # launcher.main()
    UI(Island(controls={})).run()
