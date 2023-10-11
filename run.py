from spirit_island import launcher
from spirit_island.ui.ui import UI
from spirit_island.framework.island import Island

if __name__ == "__main__":
    """To run from console"""
    # launcher.main()
    UI(Island(controls={})).run()
