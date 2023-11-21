import os
import traceback

import pygame

from concurrent.futures import ThreadPoolExecutor

from spirit_island.framework.input_request import InputHandler
from spirit_island.framework.logger import logger
from spirit_island.launcher import Runner
from spirit_island.ui.component.button import TextButton
from spirit_island.ui.component.header import Header
from spirit_island.ui.island_ui import BoardComponent
from spirit_island.ui.util import SPIRIT_BOARD_BACKGROUND

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
        self.header = Header(self._runner.island, self.options["WIDTH"], header_height)
        self.worker_thread_pool = ThreadPoolExecutor(max_workers=1)

        # Next phase button
        next_phase_button = TextButton(
            "Next phase",
            self.create_worker_thread_task(self._runner.next_phase),
            offset=[0, header_height + 40],
        )
        self._current_phase_image = TextButton(
            lambda: self._runner.get_current_phase().get_name(),
            offset=[0, header_height]
        )
        self.input_required_button = TextButton(
            lambda: self._runner.get_input_request().message if self._runner.get_input_request() else "Input required",
            offset=[0, header_height + 80]
        )
        self._components = [
            self._island_ui,
            next_phase_button,
            self._current_phase_image,
            self.input_required_button,
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
