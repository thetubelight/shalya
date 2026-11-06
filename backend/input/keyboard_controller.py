import keyboard


class KeyboardController:

    def get_inputs(self):
        return {
            # "kill": keyboard.is_pressed("space"),

            "forward": keyboard.is_pressed("w"),
            "left": keyboard.is_pressed("a"),
            "backward": keyboard.is_pressed("s"),
            "right": keyboard.is_pressed("d"),
            "up": keyboard.is_pressed("up"),
            "down": keyboard.is_pressed("down"),
            "rotate-left": keyboard.is_pressed("left"),
            "rotate-right": keyboard.is_pressed("right"),
        }