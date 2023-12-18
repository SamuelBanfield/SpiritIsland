import os
import traceback
from typing import List

import pygame

from concurrent.futures import ThreadPoolExecutor

from spirit_island.framework.input_request import InputHandler
from spirit_island.framework.logger import logger
from spirit_island.launcher import Runner
from spirit_island.ui.component.button import TextButton
from spirit_island.ui.component.button_array import ButtonArray
from spirit_island.ui.component.component import UIComponent
from spirit_island.ui.component.header import Header
from spirit_island.ui.component.hand_component import HandComponent
from spirit_island.ui.island_ui import BoardComponent
from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND
from spirit_island.framework.power_cards import shadows_flicker_like_flame

pygame.init()


class UI:
    def __init__(self, options={}):
        # Path to debug controls
        controls_path = os.path.abspath(__file__ + "../../../../debug_controls.json")
        self.options = {"FPS": 60, "WIDTH": 1200, "HEIGHT": 800}
        for option in options:
            self.options[option] = options[option]
        self._input_handler = InputHandler(self.options["FPS"])
        self._runner = Runner(controls_path, self._input_handler)
        self._runner.create_island()
        self._runner.create_phases()
        self._runner.get_current_phase().execute_phase()
        header_height = self.options["HEIGHT"] // 5
        self._island_ui = BoardComponent(self._runner.island, (0, header_height), (self.options["WIDTH"], self.options["HEIGHT"]), self._input_handler)
        self._hand_component = HandComponent(
            shadows_flicker_like_flame.POWERS,
            self.options["WIDTH"] // 2,
            self.options["HEIGHT"] // 4,
            (self.options["WIDTH"] // 4, 3 * self.options["HEIGHT"] // 4),
            self._runner.island,
            self.run_safely_in_worker_thread
        )
        self.header = Header(self._runner.island, self.options["WIDTH"], header_height, self._runner)

        self.worker_thread_pool = ThreadPoolExecutor(max_workers=1)

        # Next phase button
        next_phase_button = TextButton(
            "Next phase",
            callback=self.create_worker_thread_task(self._runner.next_phase),
            offset=[0, header_height + 40],
            enablement=lambda: self._runner.get_current_phase().is_complete,
        )
        self._current_phase_image = TextButton(
            lambda: self._runner.get_current_phase().get_name(),
            offset=[0, header_height],
            enablement=lambda: False
        )
        def _mark_done():
            if self._runner.get_input_request():
                self._runner.get_input_request().resolution["complete"] = True
        self.done_button = TextButton(
            "Done",
            callback=_mark_done,
            offset=[0, header_height + 120],
            enablement=lambda: self._runner.get_input_request() and self._runner.get_input_request().user_finishable
        )
        self.buttons = ButtonArray(
            [
                next_phase_button,
                self._current_phase_image,
                self.done_button
            ],
            (
                self.options["WIDTH"] - 200,
                header_height
            ),
            200,
            self.options["HEIGHT"] // 2
        )
        self._components: List[UIComponent] = [
            self.buttons,
            self._island_ui,
            self._hand_component,
            self.header,
        ]

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle all pygame events, return whether a quit event was received.
        """
        if event.type == pygame.QUIT:
            if self._input_handler.input_request:
                self._input_handler.input_request.resolution["errors"] = "Terminating worker thread for shutdown"
            self.worker_thread_pool.shutdown(wait=True, cancel_futures=True)
            pygame.quit()
            return True
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for child in self._components:
                if child.is_location_on_component(mouse_pos):
                    child.handle_click(mouse_pos)
        return False

    def render(self, dest: pygame.Surface):
        dest.fill(SPIRIT_BOARD_BACKGROUND)
        for child in self._components:
            child.render(dest, child.is_location_on_component(pygame.mouse.get_pos()))

    def run(self):
        display = pygame.display.set_mode(
            (self.options["WIDTH"], self.options["HEIGHT"])
        )
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if self.handle_event(event):
                    return True
            self.render(display)
            pygame.display.flip()
            clock.tick(self.options["FPS"])

    def run_safely_in_worker_thread(self, task, *args, **kwargs):
        """
        :param task: callback function to be run
        :param args: arguments for the task
        :param kwargs: key word arguments for the task

        Submit a task to a worker thread

        The idea is that this task may need input from the user,
        so we run it on a worker thread so it can await user input
        which will be supplied by the UI (main) thread.

        Unfortunately, when there is an exception on a worker thread,
        it dies and doesn't tell us why, so we wrap it to print logs
        from whatever exception occurred.
        """
        def run_safely():
            try:
                task(*args, **kwargs)
            except Exception as e:
                logger.error(f"Caught exception in worker thread: {''.join(traceback.format_exception(e))}")
        self.worker_thread_pool.submit(run_safely)

    def create_worker_thread_task(self, task, *args, **kwargs):
        """
        :param task: callback function to be run
        :param args: arguments for the task
        :param kwargs: key word arguments for the task

        Create a callback that runs the given task in a worker
        thread (wraps the task so that in runs in
        a worker thread and doesn't block the UI).
        """
        return lambda: self.run_safely_in_worker_thread(task, *args, **kwargs)
