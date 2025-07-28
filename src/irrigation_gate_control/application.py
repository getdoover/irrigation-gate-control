import logging
import time

from pydoover.docker import Application
from pydoover import ui

from .app_config import IrrigationGateControlConfig
from .app_ui import IrrigationGateControlUI, get_remote_key
from .app_state import IrrigationGateControlState

log = logging.getLogger()

class IrrigationGateControlApplication(Application):
    config: IrrigationGateControlConfig  # not necessary, but helps your IDE provide autocomplete!

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.started: float = time.time()
        self.ui: IrrigationGateControlUI = None
        self.state: IrrigationGateControlState = None

    async def setup(self):
        self.ui = IrrigationGateControlUI(self)
        self.state = IrrigationGateControlState(self)
        self.ui_manager.set_display_name("Gate Controller")
        self.ui_manager.add_children(*self.ui.fetch())

        self.open_direction = self.config.open_direction.value.lower()
        self.close_direction = (
            "reverse" if self.open_direction == "forward" else "forward"
        )

        self.controlled_remote = self.config.controlled_remote.value
        self.controlled_remote_key = get_remote_key(self.controlled_remote)

        self.hydraulic_controller_name = self.config.hydraulic_controller.value

    async def main_loop(self):
        s = await self.state.spin_state()
        log.info(f"State is: {s}")


        if s == "off":
            self.ui.open_now.coerce(None)
            self.ui.close_now.coerce(None)
            await self.set_tag_async(
                f"request_{self.controlled_remote_key}",
                "off",
                self.hydraulic_controller_name,
            )

        elif s == "finished_movement":
            self.ui.open_now.coerce(None)
            self.ui.close_now.coerce(None)
            await self.set_tag_async(
                f"request_{self.controlled_remote_key}",
                "off",
                self.hydraulic_controller_name,
            )

        elif s == "error":
            await self.set_tag_async(
                f"request_{self.controlled_remote_key}",
                "off",
                self.hydraulic_controller_name,
            )

        elif s == "prep_opening":
            await self.set_tag_async(
                f"request_{self.controlled_remote_key}",
                self.open_direction,
                self.hydraulic_controller_name,
            )

        elif s == "opening":
            await self.set_tag_async(
                f"request_{self.controlled_remote_key}",
                self.open_direction,
                self.hydraulic_controller_name,
            )

        elif s == "prep_closing":
            await self.set_tag_async(
                f"request_{self.controlled_remote_key}",
                self.close_direction,
                self.hydraulic_controller_name,
            )

        elif s == "closing":
            await self.set_tag_async(
                f"request_{self.controlled_remote_key}",
                self.close_direction,
                self.hydraulic_controller_name,
            )

    def has_open_command(self):
        print("has_open_command: ", str(self.ui.open_now.current_value))
        return self.ui.open_now.current_value

    def has_close_command(self):
        return self.ui.close_now.current_value

    def is_open_ready(self):
        return (
            self.get_tag(f"{self.controlled_remote_key}", self.hydraulic_controller_name) == self.open_direction
        )

    def is_close_ready(self):
        return (
            self.get_tag(f"{self.controlled_remote_key}", self.hydraulic_controller_name) == self.close_direction
        )

    def is_remote_off(self):
        return (
            self.get_tag(f"{self.controlled_remote_key}", self.hydraulic_controller_name) == "off"
        )
