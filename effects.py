# effects.py

import uasyncio as asyncio

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 180, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OFF = (0, 0, 0)


async def flash_all(np, color, times=3, delay=0.15):
    for _ in range(times):
        np.on(color)
        await asyncio.sleep(delay)
        np.clear()
        await asyncio.sleep(delay)


async def win_animation(np):
    await flash_all(np, WHITE, times=1, delay=0.08)
    await flash_all(np, RED, times=2, delay=0.1)


async def lose_animation(np):
    await flash_all(np, YELLOW, times=3, delay=0.15)


async def level_up_animation(np, level):
    np.clear()

    for i in range(level):
        np.np[i] = np.scale(GREEN)

    np.np.write()
    await asyncio.sleep(0.6)
    np.clear()


async def final_win_animation(np):
    colors = [RED, GREEN, BLUE, YELLOW, WHITE]

    # Run three major animation cycles
    for _ in range(5):

        # 1. Full-strip color flashes
        for color in colors:
            np.on(color)
            await asyncio.sleep(0.10)

        # 2. Forward scanner
        for i in range(np.n):
            np.clear()
            np.np[i] = np.scale(WHITE)
            if i > 0:
                np.np[i - 1] = np.scale(BLUE)
            np.np.write()
            await asyncio.sleep(0.04)

        # 3. Reverse scanner
        for i in range(np.n - 1, -1, -1):
            np.clear()
            np.np[i] = np.scale(WHITE)
            if i < np.n - 1:
                np.np[i + 1] = np.scale(RED)
            np.np.write()
            await asyncio.sleep(0.04)

        # 4. Rotating rainbow bands
        for shift in range(np.n):
            for i in range(np.n):
                np.np[i] = np.scale(colors[(i + shift) % len(colors)])
            np.np.write()
            await asyncio.sleep(0.05)

    # Grand finale
    await flash_all(np, WHITE, times=4, delay=0.10)
    np.on(RED)
    await asyncio.sleep(0.35)
    np.clear()


