# Responsible for:

# Current Roll
# Current Pitch
# Current Yaw
# Current Throttle

from dataclasses import dataclass, asdict
import json
import time


@dataclass
class ControlState:
    timestamp: float
    roll: float
    pitch: float
    yaw: float
    throttle: float

    def to_json(self) -> str:
        return json.dumps({
            "type": "control_state",
            "timestamp": self.timestamp,
            "roll": self.roll,
            "pitch": self.pitch,
            "yaw": self.yaw,
            "throttle": self.throttle
        })


class StateManager:

    def __init__(self):
        self.state = ControlState(
            timestamp=time.time(),
            roll=0.0,
            pitch=0.0,
            yaw=0.0,
            throttle=0.0
        )

    def get_state(self) -> ControlState:
        return self.state

    def update_state(
        self,
        roll: float,
        pitch: float,
        yaw: float,
        throttle: float
    ) -> None:
        self.state = ControlState(
            timestamp=time.time(),
            roll=roll,
            pitch=pitch,
            yaw=yaw,
            throttle=throttle
        )