# main.py

import uasyncio as asyncio
from machine import Pin
from async_switch import Switch
from neopixel_helper import NP
from effects import win_animation, lose_animation, level_up_animation, final_win_animation
from sounds import win_sound, lose_sound, restart_sound, level_up_sound, final_win_song

np = NP(pin_num=14, led_count=18)

level = 1
max_level = 4

current_index = 0
direction = 1
running = True
round_over = False
game_complete = False
result_task = None

speeds = {
    1: 0.04,
    2: 0.032,
    3: 0.025,
    4: 0.018
}


def get_red_zone():
    red_size = 6 - (level - 1)
    return range(0, red_size)


async def win_round():
    global level, running, round_over, game_complete

    await asyncio.gather(
        win_animation(np),
        win_sound()
    )

    if level == max_level:
        game_complete = True
        await asyncio.gather(
            final_win_animation(np),
            final_win_song()
        )
    else:
        level += 1
        await asyncio.gather(
            level_up_animation(np, level),
            level_up_sound()
        )

    round_over = True


async def lose_round():
    await asyncio.gather(
        lose_animation(np),
        lose_sound()
    )


def reset_round():
    global current_index, direction, running, round_over

    current_index = 0
    direction = 1
    running = True
    round_over = False


def reset_game():
    global level, game_complete

    level = 1
    game_complete = False
    reset_round()


def button_pressed():
    global running, round_over, result_task

    if running:
        running = False
        round_over = True

        if current_index in get_red_zone():
            print("WIN! Level", level)
            result_task = asyncio.create_task(win_round())
        else:
            print("Try again!")
            result_task = asyncio.create_task(lose_round())

    elif round_over or game_complete:
        print("Restarting...")

        if result_task:
            result_task.cancel()

        asyncio.create_task(restart_sound())

        if game_complete:
            reset_game()
        else:
            reset_round()


async def game_loop():
    global current_index, direction

    while True:
        if running:
            np.draw_board(current_index, red_size=6 - (level - 1))

            current_index += direction

            if current_index == 17:
                direction = -1
            elif current_index == 0:
                direction = 1

        await asyncio.sleep(speeds[level])


async def main():
    button = Switch(Pin(18, Pin.IN, Pin.PULL_UP))
    button.close_func(button_pressed)

    await asyncio.sleep(0.2)
    await restart_sound()

    await game_loop()


try:
    asyncio.run(main())
finally:
    np.clear()
    print("goodbye")
