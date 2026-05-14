# sounds.py

import uasyncio as asyncio
from machine import Pin, PWM
from rtttl import RTTTL

buzzer = PWM(Pin(25))
buzzer.duty_u16(0)


async def play_tone(freq, duration):
    if freq > 0:
        buzzer.freq(int(freq))
        buzzer.duty_u16(2000)
    else:
        buzzer.duty_u16(0)

    await asyncio.sleep(duration)

    buzzer.duty_u16(0)


async def play_rtttl(tune):
    song = RTTTL(tune)

    for freq, msec in song.notes():
        # RTTTL returns milliseconds; convert to seconds
        await play_tone(freq, msec / 1000.0)
        await asyncio.sleep(0.02)

    buzzer.duty_u16(0)


async def win_sound():
    await play_rtttl(
        "Win:d=8,o=5,b=180:c,e,g,c6"
    )


async def lose_sound():
    await play_rtttl(
        "Lose:d=4,o=4,b=100:c,p,c3"
    )


async def restart_sound():
    await play_rtttl(
        "Restart:d=16,o=5,b=220:g"
    )


async def level_up_sound():
    await play_rtttl(
        "LevelUp:d=16,o=5,b=200:e,g,b"
    )


async def final_win_song():
    await play_rtttl(
        "SWEnd:d=4,o=5,b=225:"
        "2c,1f,2g.,8g#,8a#,1g#,2c.,c,2f.,g,g#,c,"
        "8g#.,8c.,8c6,1a#.,2c,2f.,g,g#.,8f,c.6,"
        "8g#,1f6,2f,8g#.,8g.,8f,2c6,8c.6,8g#.,8f,"
        "2c,8c.,8c.,8c,2f,8f.,8f.,8f,2f"
    )
