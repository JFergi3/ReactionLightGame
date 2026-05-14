# 🎮 Reaction Light Game (MicroPython on ESP32)

## Project Summary

The **Reaction Light Game** is a four-level arcade-style reaction game built with an ESP32 microcontroller, an 18-LED NeoPixel strip, a push button, and a piezo buzzer.

A white "scanner" light moves back and forth across a color-coded LED strip. The player presses a button to stop the light in the red target zone.

* If the light stops in the red zone, the player wins the level.
* Each level becomes harder by:

  * Increasing the light speed
  * Shrinking the red target zone
* After completing all four levels, the game plays a Star Wars-inspired victory song and a multi-stage LED celebration.

This project demonstrates modular programming, asynchronous programming, hardware control, and game state management.

---

# 🧰 Hardware Used

| Component                 | Description                          |
| ------------------------- | ------------------------------------ |
| ESP32                     | Main microcontroller                 |
| WS2812B / NeoPixel Strip  | 18 individually addressable RGB LEDs |
| Push Button               | Starts, stops, and restarts the game |
| Piezo Buzzer              | Plays sound effects and songs        |
| Breadboard + Jumper Wires | Circuit assembly                     |

---

# 💻 Software Used

| Software                                                                                     | Purpose                                   |
| -------------------------------------------------------------------------------------------- | ----------------------------------------- |
| entity["software","Thonny","Python IDE"]                                                  | Writing and uploading code                |
| entity["programming_language","MicroPython","Python implementation for microcontrollers"] | Programming language running on the ESP32 |
| `uasyncio`                                                                                   | Cooperative multitasking                  |
| `neopixel`                                                                                   | LED strip control                         |
| `machine`                                                                                    | Hardware access (GPIO, PWM)               |
| `async_switch`                                                                               | Non-blocking button handling              |
| `rtttl.py`                                                                                   | Ring Tone Transfer Language music parser  |

---

# 📁 Project Structure

```text
Reaction-Light-Game/
│
├── main.py
├── neopixel_helper.py
├── effects.py
├── sounds.py
├── rtttl.py
├── async_switch.py
└── README.md
```

---

# 📄 File Responsibilities

## `main.py`

Contains the core game logic:

* Tracks current level
* Moves the scanner light
* Detects button presses
* Determines win or loss
* Controls level progression
* Coordinates animations and sounds

## `neopixel_helper.py`

Encapsulates LED strip logic:

* Initializes the NeoPixel strip
* Draws the game board
* Applies global brightness scaling
* Displays the moving LED and trailing effect

## `effects.py`

Contains all LED animations:

* Win flashes
* Lose flashes
* Level-up indicators
* Final victory light show

## `sounds.py`

Handles all buzzer playback:

* Win and lose tones
* Restart beep
* Level-up fanfare
* Final Star Wars-inspired melody

## `rtttl.py`

Parses RTTTL strings and converts them into note frequencies and durations.

---

# 🎮 Gameplay Overview

## Level 1

* Red target zone = 6 LEDs
* Slow speed

## Level 2

* Red target zone = 5 LEDs
* Faster speed

## Level 3

* Red target zone = 4 LEDs
* Faster speed

## Level 4

* Red target zone = 3 LEDs
* Fastest speed

## Final Victory

* Plays a long RTTTL song
* Runs a multi-phase LED show

---

# 🔌 Pin Assignments

| ESP32 Pin | Component     |
| --------- | ------------- |
| GPIO 14   | NeoPixel Data |
| GPIO 18   | Push Button   |
| GPIO 25   | Piezo Buzzer  |

---

# 🧠 Programming Concepts Used

## Object-Oriented Programming (OOP)

The `NP` class in `neopixel_helper.py` wraps all LED operations.

```python
class NP:
    def __init__(self, pin_num=14, led_count=18, brightness=0.15):
        self.n = led_count
        self.brightness = brightness
```

### Why This Matters

Instead of writing LED logic throughout the project, we group related behavior into one class.

Benefits:

* Reusability
* Encapsulation
* Easier debugging
* Cleaner code

---

# 🔒 Encapsulation

Methods such as:

* `clear()`
* `on()`
* `draw_board()`
* `scale()`

hide the implementation details from the rest of the program.

The main game can simply call:

```python
np.draw_board(current_index, red_size=5)
```

without needing to know how the LEDs are updated.

---

# 🎨 Brightness Scaling

NeoPixels can be extremely bright. A brightness factor was added to scale every RGB value.

```python
def scale(self, color):
    return tuple(int(c * self.brightness) for c in color)
```

### Example

```python
RED = (255, 0, 0)
brightness = 0.15

# Result: (38, 0, 0)
```

### Why This Is Useful

* Reduces eye strain
* Lowers power consumption
* Makes colors look smoother

---

# 🔁 Global Variables

The game uses several global variables to track state.

```python
level = 1
running = True
round_over = False
game_complete = False
current_index = 0
direction = 1
```

### Purpose

| Variable        | Meaning                  |
| --------------- | ------------------------ |
| `level`         | Current difficulty level |
| `running`       | Scanner is moving        |
| `round_over`    | Waiting for restart      |
| `game_complete` | Player beat all levels   |
| `current_index` | Current LED position     |
| `direction`     | Movement direction       |

---

# 🌍 `global` Keyword

When modifying a global variable inside a function, Python requires the `global` keyword.

```python
def reset_round():
    global current_index, direction, running
```

Without this, Python would create local variables instead of modifying the shared game state.

---

# 🔄 Infinite Game Loop

```python
while True:
```

This loop runs forever while the microcontroller is powered.

Inside the loop:

1. Draw the board
2. Move the scanner
3. Reverse at the ends
4. Pause briefly

---

# ↔️ Direction Control

```python
current_index += direction
```

If `direction = 1`, the scanner moves right.
If `direction = -1`, the scanner moves left.

```python
if current_index == 17:
    direction = -1
elif current_index == 0:
    direction = 1
```

This creates a bouncing motion.

---

# ⏱️ `await asyncio.sleep()` Controls Speed

```python
await asyncio.sleep(0.04)
```

Smaller numbers make the light move faster.

### Difficulty Table

```python
speeds = {
    1: 0.04,
    2: 0.032,
    3: 0.025,
    4: 0.018
}
```

---

# ⚡ Asynchronous Programming with `uasyncio`

`uasyncio` allows multiple tasks to run cooperatively.

Examples:

* Moving LEDs
* Playing music
* Responding to button presses

---

# 🚀 Creating Tasks

```python
asyncio.create_task(win_round())
```

Starts a function in the background without blocking the program.

---

# 🤝 Running Tasks in Parallel

```python
await asyncio.gather(
    win_animation(np),
    win_sound()
)
```

Both functions run simultaneously.

This allows the LEDs and buzzer to stay synchronized.

---

# 🔘 Event-Driven Button Handling

```python
button.close_func(button_pressed)
```

Registers `button_pressed()` as a callback.

When the button is pressed, the function is called automatically.

This is more efficient than constantly polling the button.

---

# 🏆 Dynamic Red Zone

```python
def get_red_zone():
    red_size = 6 - (level - 1)
    return range(0, red_size)
```

### Red Zone Sizes

| Level | Red LEDs |
| ----: | -------: |
|     1 |        6 |
|     2 |        5 |
|     3 |        4 |
|     4 |        3 |

---

# 🎵 RTTTL Music

RTTTL (Ring Tone Transfer Language) stores melodies as strings.

```python
"Win:d=8,o=5,b=180:c,e,g,c6"
```

### Meaning

| Part       | Meaning                  |
| ---------- | ------------------------ |
| `d=8`      | Default eighth notes     |
| `o=5`      | Default octave 5         |
| `b=180`    | Tempo (beats per minute) |
| `c,e,g,c6` | Notes to play            |

---

# 🔊 PWM Audio

The buzzer uses Pulse Width Modulation.

```python
buzzer = PWM(Pin(25))
buzzer.freq(440)
buzzer.duty_u16(2000)
```

This creates a 440 Hz tone.

---

# 🌈 Final Victory Show

The final animation combines:

* Full-strip color flashes
* Forward and reverse scanners
* Rainbow cycling
* Theater chase effects
* Grand finale flashes

The animation runs in parallel with the Star Wars-inspired ending song.

---

# 🧩 Development Path

This project evolved incrementally.

## Phase 1: Basic Scanner

* White LED moved back and forth

## Phase 2: Color Zones

* Red, green, and blue sections added

## Phase 3: Stop Button

* Button stopped the scanner

## Phase 4: Win/Lose Logic

* Red zone detection

## Phase 5: Restart Button

* Same button restarts the round

## Phase 6: Modular Refactoring

* Split code into helper modules

## Phase 7: Sounds

* Added buzzer effects

## Phase 8: Level System

* Four increasing difficulty levels

## Phase 9: RTTTL Music

* Added melody support

## Phase 10: Final Celebration

* Long synchronized LED and audio finale

---

# ▶️ Running the Project

1. Connect the ESP32 to your computer.
2. Open the project in entity["software","Thonny","Python IDE"].
3. Upload all files to the board.
4. Run `main.py`.
5. Press the button to stop the scanner.
6. Win all four levels.

---

# 📚 Key Lessons Learned

* How to organize code across multiple files
* How to use classes and encapsulation
* How asynchronous programming works
* How to synchronize sound and animation
* How to scale LED brightness
* How to build a complete game loop
* How to parse and play RTTTL melodies

---

# 🚀 Future Improvements

* OLED score display
* High score tracking
* Additional game modes
* Randomized target zone
* Difficulty selection menu
* Multiplayer support

---

# 👨‍💻 Author

Jake Ferguson

Student at Waukesha County Technical College (WCTC)
Pursuing an AAS in Web & Software Development

---

# 📄 License

This project is provided for educational and portfolio purposes.
