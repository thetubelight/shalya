
import asyncio
from backend.shared_state import state_manager
from backend.input.keyboard_controller import KeyboardController


UPDATE_RATE_HZ = 20

CONTROL_INCREMENT = 0.8 #for gesture, use something like 0.05, for keyboard use bigger value(closer to 1)
RETURN_INCREMENT = 0.8  #these changes are temporary, values might change during tuning
#also note that for gesture control, we would need filtering, i'll use ema for smoothness and alpha = 0.3 approx
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def return_to_zero(value):
    if abs(value) < RETURN_INCREMENT:
        return 0.0

    if value > 0:
        return value - RETURN_INCREMENT

    if value < 0:
        return value + RETURN_INCREMENT

    return value


class ControlLoop:

    def __init__(self):
        self.controller = KeyboardController()

        self.roll = 0.0
        self.pitch = 0.0
        self.throttle = 0.0
        self.yaw = 0.0
    
    def update_inputs(self):
        inputs = self.controller.get_inputs()
        #check kill input condition
        # if inputs["kill"]:
        #     self.roll = 0.0
        #     self.pitch = 0.0
        #     self.throttle = 0.0
        #     self.yaw = 0.0

        #     print("Kill input detected. Exiting control loop...")
        #     return

        # Pitch Control
        if inputs["forward"]:
            self.pitch += CONTROL_INCREMENT

        if inputs["backward"]:
            self.pitch -= CONTROL_INCREMENT

        # No pitch input -> return to center
        if not inputs["forward"] and not inputs["backward"]:
            self.pitch = return_to_zero(self.pitch)

        # Roll Control
        if inputs["left"]:
            self.roll -= CONTROL_INCREMENT

        if inputs["right"]:
            self.roll += CONTROL_INCREMENT

        # No roll input -> return to center
        if not inputs["left"] and not inputs["right"]:
            self.roll = return_to_zero(self.roll)

        # throttle Control
        if inputs["up"]:
            self.throttle += CONTROL_INCREMENT

        if inputs["down"]:
            self.throttle -= CONTROL_INCREMENT

        # No throttle input -> return to center
        if not inputs["up"] and not inputs["down"]:
            self.throttle = return_to_zero(self.throttle)

        # yaw Control
        if inputs["rotate-left"]:
            self.yaw -= CONTROL_INCREMENT

        if inputs["rotate-right"]:
            self.yaw += CONTROL_INCREMENT

        # No yaw input -> return to center
        if not inputs["rotate-left"] and not inputs["rotate-right"]:
            self.yaw = return_to_zero(self.yaw)

        # Clamp values
        self.pitch = clamp(self.pitch, -1.0, 1.0)
        self.roll = clamp(self.roll, -1.0, 1.0)
        self.throttle = clamp(self.throttle, -1.0, 1.0)
        self.yaw = clamp(self.yaw, -1.0, 1.0)
        
    def update_state(self):

        state_manager.update_state(
            roll=self.roll,
            pitch=self.pitch,
            yaw=self.yaw,
            throttle=self.throttle
        )
        print(
            f"Roll={self.roll:.2f} "
            f"Pitch={self.pitch:.2f} "
            f"Yaw={self.yaw:.2f} "
            f"Throttle={self.throttle:.2f}"
        )
    
    async def run(self):

        while True:
            self.update_inputs()

            self.update_state()
            # if self.controller.get_inputs()["kill"]:
            #     print("Control loop terminated by kill input.")
            #     break

            await asyncio.sleep(1 / UPDATE_RATE_HZ)