import logging

from pydoover.state import StateMachine

log = logging.getLogger(__name__)

class IrrigationGateControlState:
    state: str

    prep_timeout_secs = 60 * 2  # 2 minutes
    error_timeout_secs = 60 * 60 * 24  # 24 hours

    # Keep transitions at class level since they don't depend on config
    transitions = [
        {"trigger": "stop", "source": "*", "dest": "off"},
        {"trigger": "start_opening", "source": "off", "dest": "prep_opening"},
        {"trigger": "ready_open", "source": "prep_opening", "dest": "opening"},
        {"trigger": "start_closing", "source": "off", "dest": "prep_closing"},
        {"trigger": "ready_close", "source": "prep_closing", "dest": "closing"},
        {"trigger": "set_error", "source": "*", "dest": "error"},
        {"trigger": "finish_movement", "source": ["opening", "closing"], "dest": "finished_movement"},
    ]

    def __init__(self, app):
        self.app = app

        # Create states as instance attribute with proper timeout values
        self.states = [
            {"name": "off"},
            {
                "name": "prep_opening",
                "timeout": self.prep_timeout_secs,
                "on_timeout": "set_error",
            },
            {
                "name": "opening",
                "timeout": self.open_timeout_secs,
                "on_timeout": "finish_movement",
            },
            {
                "name": "prep_closing",
                "timeout": self.prep_timeout_secs,
                "on_timeout": "set_error",
            },
            {
                "name": "closing",
                "timeout": self.close_timeout_secs,
                "on_timeout": "finish_movement",
            },
            {"name": "error", "timeout": self.error_timeout_secs, "on_timeout": "stop"},
            {"name": "finished_movement", "timeout": 5, "on_timeout": "stop"},
        ]

        self.state_machine = StateMachine(
            states=self.states,
            transitions=self.transitions,
            model=self,
            initial="off",
            queued=True,
        )

    @property
    def open_timeout_secs(self):
        return self.app.config.open_timeout.value
    
    @property
    def close_timeout_secs(self):
        return self.app.config.close_timeout.value

    async def spin_state(self):
        last_state = None
        ## keep spinning until state has stabilised
        while last_state != self.state:
            last_state = self.state
            await self.evaluate_state()
            # log.info(f"State spin complete for {self.name} - {self.state}")
        return self.state

    async def evaluate_state(self):
        s = self.state

        if s in ["off", "error"]:
            if self.app.has_open_command():
                await self.start_opening()
            elif self.app.has_close_command():
                await self.start_closing()

        elif s == "finished_movement":
            if not self.app.has_open_command() and not self.app.has_close_command() and self.app.is_remote_off():
                await self.stop()

        elif s == "prep_opening":
            if not self.app.has_open_command():
                await self.finish_movement()
            if self.app.is_open_ready():
                await self.ready_open()

        elif s == "opening":
            if not self.app.has_open_command():
                await self.finish_movement()
            if not self.app.is_open_ready():
                await self.finish_movement()

        elif s == "prep_closing":
            if not self.app.has_close_command():
                await self.finish_movement()
            if self.app.is_close_ready():
                await self.ready_close()

        elif s == "closing":
            if not self.app.has_close_command():
                await self.finish_movement()
            if not self.app.is_close_ready():
                await self.finish_movement()
