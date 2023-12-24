import pygame


class UIComponent:
    def __init__(self):
        pass

    def render(self, dest: pygame.surface.Surface, hovered: bool):
        """
        :param dest: the parent component's surface
        :param hovered: whether the mouse is hovering over this component
        Render the component to the given surface.
        """
        # Hovered should be adjusted not to be a boolean, since we
        # would like to pass it down to child components
        pass

    def handle_click(self, click_location):
        """
        :param click_location: the location of the click
        """
        pass

    def is_location_on_component(self, location) -> bool:
        """
        :param location: the location of the mouse (inconsistentenly relative to this component
        or the parent component)
        """
        pass

    def update(self):
        """
        Called every frame to update the component's state.
        """
        pass
