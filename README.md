# SpiritIsland

Requirements:
python 3.10

# Model

The entry point to the model is `spirit_island.framework.island.Island`. The model is driven by a runner, which does things like execute invader phases. It also makes requests for user input when required, by delegating to an input handler.

# UI

The UI is split up into UIComponents, which may be nested. Each component overrides some methods:

* render() which draws to the component to its parents pygame surface (which is eventually drawn to the screen)
* handle_click() which handles clicks, including by delegating to any child components
* is_location_on_component() which returns a boolean whether the mouse location is on the component, this is called to check whether the handle_click method should then be called. The mouse location is inconsistently either relative to the top left of the current component or the parent component

The general pattern for the UI components is we wrap a UI object around a model object. For example, we have the Island object in the framework package, which is wrapped by a BoardComponent in the UI. The framework object holds all the data, and the UI object reads the data in order to display it, but doesn't make any direct changes. Another simpler example is the FearComponent which wraps the TerrorHandler.

# Threading

The main thread is the UI thread, which runs a loop at FPS times a second. This does two main things:

* Reads pygame events like key presses, mouse movements and clicks
* Draws the UI by reading our instance of Island

It should not make direct changes to the Island itself to ensure thread safety.

Changes to the Island itself are made in worker threads, which are created by a thread pool executor attached to the runner. This is so that the worker threads can sit awaiting user input, without preventing updates to the UI.

# Spirit powers

See `spirit_island.framework.power_cards.power_card_base.SpiritPower`, which I'm hoping is general enough to be used for both power cards and innates. The idea is the logic of the power card is extracted to a single function, which is passed in as a callback. See `spirit_island.framework.power_cards.shadows_flicker_like_flame` for examples.
