#!/usr/bin/env python3
import random
import shutil
import sys
import time

CHARS = " .:-=+*#%@$"


def heat_to_rgb(heat):
    if heat <= 0:
        return 0, 0, 0
    elif heat < 85:
        return int(heat * 3), 0, 0
    elif heat < 170:
        return 255, int((heat - 85) * 3), 0
    else:
        t = heat - 170
        return 255, 165 + int(t * 90 / 85), int(t * 255 / 85)


def heat_to_char(heat):
    return CHARS[int(heat / 255 * (len(CHARS) - 1))]


def main():
    sys.stdout.write("\033[?25l")  # hide cursor
    sys.stdout.flush()

    try:
        cols, rows = shutil.get_terminal_size()
        fire = [[0] * cols for _ in range(rows)]

        while True:
            cols, rows = shutil.get_terminal_size()
            if len(fire) != rows or len(fire[0]) != cols:
                fire = [[0] * cols for _ in range(rows)]

            # Fuel: randomize bottom row
            for x in range(cols):
                fire[rows - 1][x] = random.randint(180, 255) if random.random() > 0.05 else 0

            # Propagate heat upward with cooling
            for y in range(rows - 2, -1, -1):
                for x in range(cols):
                    total = (
                        fire[y + 1][(x - 1) % cols]
                        + fire[y + 1][x]
                        + fire[y + 1][(x + 1) % cols]
                        + fire[min(y + 2, rows - 1)][x]
                    )
                    fire[y][x] = max(0, total // 4 - random.randint(0, 6))

            # Render frame
            sys.stdout.write("\033[H")
            buf = []
            for y in range(rows - 1):
                row = []
                for x in range(cols):
                    h = fire[y][x]
                    r, g, b = heat_to_rgb(h)
                    row.append(f"\033[38;2;{r};{g};{b}m{heat_to_char(h)}")
                buf.append("".join(row))
            sys.stdout.write("\n".join(buf))
            sys.stdout.flush()

            time.sleep(1 / 30)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[0m\033[?25h\033[2J\033[H")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
