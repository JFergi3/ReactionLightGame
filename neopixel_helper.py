# neopixel_helper.py

import neopixel
from machine import Pin


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
TRAIL = (80, 80, 80)
OFF = (0, 0, 0)


class NP:
    def __init__(self, pin_num=14, led_count=18, brightness=0.15):
        self.n = led_count
        self.brightness = brightness
        self.np = neopixel.NeoPixel(Pin(pin_num), led_count)
        
    def scale(self,color):
        return tuple(int(c * self.brightness) for c in color)

    def clear(self):
        for i in range(self.n):
            self.np[i] = OFF
        self.np.write()

    def on(self, color):
        for i in range(self.n):
            self.np[i] = color
        self.np.write()

    def draw_board(self, active_index, red_size=6):
        # red zone (WIN)
        for i in range(0, red_size):
            self.np[i] = self.scale(RED)

        # green zone
        for i in range(red_size, 12):
            self.np[i] = self.scale(GREEN)

        # blue zone
        for i in range(12, 18):
            self.np[i] = self.scale(BLUE)

        # trailing glow behind the moving LED
        previous_index = active_index - 1

        if previous_index >= 0:
            self.np[previous_index] = TRAIL

        # moving light
        self.np[active_index] = self.scale(WHITE)

        self.np.write()
