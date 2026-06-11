import logging

from pydoover import ui
from pydoover.docker import Application

from .app_config import IrrigationGateControlConfig
from .app_state import IrrigationGateControlState
from .app_tags import IrrigationGateControlTags
from .app_ui import IrrigationGateControlUI

log = logging.getLogger()


def get_remote_key(remote):
    return remote.lower().replace(" ", "_")


class IrrigationGateControlApplication(Application):
    config: IrrigationGateControlConfig  # not necessary, but helps your IDE provide autocomplete!
    tags: IrrigationGateControlTags
    ui: IrrigationGateControlUI

    config_cls = IrrigationGateControlConfig
    tags_cls = IrrigationGateControlTags
    ui_cls = IrrigationGateControlUI

    async def setup(self):
        self.state = IrrigationGateControlState(self)

        self.open_direction = self.config.open_direction.value.lower()
        self.close_direction = (
            "reverse" if self.open_direction == "forward" else "forward"
        )

        self.controlled_remote_key = get_remote_key(self.config.controlled_remote.value)
        self.hydraulic_controller_name = self.config.hydraulic_controller.value

    async def main_loop(self):
        await self.process_state()

    async def process_state(self):
        s = await self.state.spin_state()
        log.info(f"State is: {s}")
        await self.tags.gate_state.set(s)

        if s in ("off", "finished_movement", "error"):
            await self.set_remote_request("off")

        elif s in ("prep_opening", "opening"):
            await self.set_remote_request(self.open_direction)

        elif s in ("prep_closing", "closing"):
            await self.set_remote_request(self.close_direction)

    async def set_remote_request(self, value: str):
        await self.set_tag(
            f"request_{self.controlled_remote_key}",
            value,
            self.hydraulic_controller_name,
        )

    @ui.handler("open_now")
    async def on_open_now(self, ctx, value):
        log.info("Open Now command received")
        await self.state.request_open()
        # process straight away rather than waiting for the next main loop
        await self.process_state()

    @ui.handler("close_now")
    async def on_close_now(self, ctx, value):
        log.info("Close Now command received")
        await self.state.request_close()
        await self.process_state()

    def remote_state(self):
        return self.get_tag(self.controlled_remote_key, self.hydraulic_controller_name)

    def is_open_ready(self):
        return self.remote_state() == self.open_direction

    def is_close_ready(self):
        return self.remote_state() == self.close_direction

    def is_remote_off(self):
        return self.remote_state() == "off"
