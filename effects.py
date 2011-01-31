import random
import time
import ascii8x8

# A dictionary of hsv values for some common colors.
colors = {"black":(0, 0, 0), "white":(0, 0, 1), "gray":(0, 0, 0.5),
          "red":(0, 1, 1), "blue":(0.66, 1, 1), "yellow":(0.16, 1, 1),
          "purple":(0.85, 1, 0.5), "green":(0.33, 1, 0.5),
          "orange":(0.083, 1, 1), "pink":(0.9, 1, 1), "lime":(0.33, 1, 1),
          "baby blue":(0.66, 0.5, 1), "cyan":(0.5, 1, 1),
          "brown":(0.07, 0.86, 0.54), "beige":(0.083, 0.32, 1),
          "indigo":(0.75, 1, 0.5), "dark gray":(0, 0, 0.15),
          "light gray":(0, 0, 0.75), "maroon":(0, 1, 0.5),
          "navy":(0.66, 1, 0.25)}

class Effect(object):
    def __init__(self, wall):
        self.wall = wall
        self.wall.clear()

    def run(self):
        pass

class SolidColorTest(Effect):
    def run(self):
        hue = 1
        saturation = 1
        value = 1

        hsv = (hue, saturation, value)
        for x in range(self.wall.width):
            for y in range(self.wall.height):
                self.wall.set_pixel(x, y, hsv)

        self.wall.draw()
        time.sleep(2)

class HueTest(Effect):
    def run(self):
        hue = random.random()
        start_time = time.time()
        while time.time() - start_time < 5:
            hsv = (hue, 1, 1)
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            hue = (hue + .01) % 1
            time.sleep(.05)

class SaturationTest(Effect):
    def run(self):
        hue = random.random()
        saturation = 0
        start_time = time.time()
        while time.time() - start_time < 5:
            hsv = (hue, saturation, 1)
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            saturation = (saturation + .05) % 1
            time.sleep(.05)

class ValueTest(Effect):
    def run(self):
        hue = random.random()
        value = 0
        start_time = time.time()
        while time.time() - start_time < 5:
            hsv = (hue, 1, value)
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            value = (value + .05) % 1
            time.sleep(.05)

class DictionaryTest(Effect):
    def run(self):
        for color in colors.keys():
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, colors[color])
            self.wall.draw()
            time.sleep(0.5)

class Checkerboards(Effect):
    def run(self):
        for i in range(10):
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    if (x + y + i) % 2 == 0:
                        self.wall.set_pixel(x, y, colors["black"])
                    else:
                        self.wall.set_pixel(x, y, colors["yellow"])
            self.wall.draw()
            time.sleep(0.5)

class Columns(Effect):
    def run(self):
        hue = random.random()
        start_time = time.time()
        while time.time() - start_time < 5:
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    hsv = (hue, 1, 1)
                    self.wall.set_pixel(x, y, hsv)
                    self.wall.draw()
                    time.sleep(.02)
                    self.wall.clear()
                    hue = (hue + .05) % 1

class Rainbow(Effect):
    def run(self):
        hue = random.random()
        hue_spacing = 1.0/(self.wall.width * self.wall.height)
        delay = .1

        # Draw rainbow stripes from right to left.
        for i in range(self.wall.width - 1, -1, -1):
            for j in range(self.wall.height - 1, -1, -1):
                hsv = (hue, 1, 1)
                self.wall.set_pixel(i, j, hsv)
                hue += hue_spacing
                # on python 2.5, having a hue value of > 1 will return None
                # when you try to convert HSV to RGB using colorsys
                #
                # in later versions, colorsys will treat a hue value of
                # > 1 as *just the truncated fractional part*, e.g.
                # 1.29 becomes 0.29.
                #
                # neither of these particularly make sense, but let's
                # emulate the behaviour of python 2.6+ here for compatibility's
                # sake.
                if hue > 1:
                    hue -= int(hue)
            time.sleep(delay)
            self.wall.draw()

        time.sleep(1)

        # Shift the wall hues for a few seconds.
        start_time = time.time()
        while time.time() - start_time < 5:
            for i in range(self.wall.width):
                for j in range(self.wall.height):
                    hsv = self.wall.get_pixel(i, j)
                    new_hue = (hsv[0] + hue_spacing/4) % 1
                    new_hsv = (new_hue, hsv[1], hsv[2])
                    self.wall.set_pixel(i, j, new_hsv)
            self.wall.draw()

        time.sleep(1)


class Twinkle(Effect):
    def run(self):
        start_time = time.time()
        while time.time() - start_time < 5:
            x = random.randint(0, self.wall.width - 1)
            y = random.randint(0, self.wall.height - 1)
            # Stick to blueish colors.
            hue = .65 + random.uniform(-1, 1) * .1
            value = random.random()
            hsv = (hue, 1, value)
            self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            time.sleep(.01)

class KnightMoves(Effect):
    def __init__(self, wall):
        self.wall = wall
        self.wall.clear()
        for x in range(self.wall.width):
            for y in range(self.wall.height):
                if (x + y) % 2 == 0:
                    self.wall.set_pixel(x, y, colors["black"])
                else:
                    self.wall.set_pixel(x, y, colors["white"])
        # Pick a random starting location for the knight
        self.knight_x = random.randint(0, self.wall.width - 1)
        self.knight_y = random.randint(0, self.wall.height - 1)
        self.wall.set_pixel(self.knight_x, self.knight_y, colors["red"])

    def run(self):
        if self.wall.width < 2 or self.wall.height < 2:
            return

        self.wall.draw()
        start_time = time.time()
        while time.time() - start_time < 12:
            self.move()
            self.wall.draw()
            time.sleep(0.75)

    def move(self):
        """
        Move the knight.
        """
        if (self.knight_x + self.knight_y) % 2 == 0:
            self.wall.set_pixel(self.knight_x, self.knight_y, colors["black"])
        else:
            self.wall.set_pixel(self.knight_x, self.knight_y, colors["white"])
        moves = self.getMoves()
        # Select a move at random from the possible moves
        self.knight_x, self.knight_y = moves[random.randint(0, len(moves) - 1)]
        self.wall.set_pixel(self.knight_x, self.knight_y, colors["red"])

    def getMoves(self):
        """
        Get all possible moves that the knight can make.
        """
        moves = []
        # Don't want knight to wrap around the board because you can't
        # do that in chess
        if (self.knight_x - 2) >= 0 and (self.knight_y - 1) >= 0:
            moves.append((self.knight_x - 2, self.knight_y - 1))
        if (self.knight_x - 1) >= 0 and (self.knight_y - 2) >= 0:
            moves.append((self.knight_x - 1, self.knight_y - 2))
        if (self.knight_x - 2) >= 0 and (self.knight_y + 1) < self.wall.height:
            moves.append((self.knight_x - 2, self.knight_y + 1))
        if (self.knight_x + 1) < self.wall.width and (self.knight_y - 2) >= 0:
            moves.append((self.knight_x + 1, self.knight_y - 2))
        if (self.knight_x - 1) >= 0 and (self.knight_y + 2) < self.wall.height:
            moves.append((self.knight_x - 1, self.knight_y + 2))
        if (self.knight_x + 2) < self.wall.width and (self.knight_y - 1) >= 0:
            moves.append((self.knight_x + 2, self.knight_y - 1))
        if (self.knight_x + 2) < self.wall.width and \
          (self.knight_y + 1) < self.wall.height:
            moves.append((self.knight_x + 2, self.knight_y + 1))
        if (self.knight_x + 1) < self.wall.width and \
          (self.knight_y + 2) < self.wall.height:
            moves.append((self.knight_x + 1, self.knight_y + 2))
        return moves

class LetterTest(Effect):
    """
    Cycle through the letters of the alphabet.

    Minimum wall size: 8 x 8.
    """
    def run(self):
        if self.wall.width < 8 or self.wall.height < 8:
            return

        color = random.random()
        foreground = (color, 1, 1)
        # Make the foreground and background complementary colors.
        background = ((color + .5) % 1, 1, 1)

        # Center the letters on the wall
        x_offset = int((self.wall.width - 8) / 2)
        y_offset = int((self.wall.height - 8) / 2)

        # Display upper and lower case letters. The break between 90 and 97 is
        # for non-letter keyboard characters.
        for ord in range(65, 91) + range(97, 123):
            self.wall.clear()

            # Set every pixel to the background color, since ascii8x8 will only
            # color an 8x8 section.
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, background)

            # Color the letter.
            ascii8x8.draw_chr(chr(ord), self.wall, foreground, background,
                              x_offset, y_offset)
            self.wall.draw()
            time.sleep(.1)

class Bouncer(Effect):
    class Ball(object):
        def __init__(self, wall):
            self.wall = wall
            self.x = random.randint(0, self.wall.width - 1)
            self.y = random.randint(0, self.wall.height - 1)
            self.hue = random.random()
            self.dx = self.dy = 0
            while self.dx == 0 and self.dy == 0:
                self.dx = random.choice([-1, 0, 1])
                self.dy = random.choice([-1, 0, 1])
            self.tail = []
            self.tail_len = 4

        def draw(self):
            self.wall.set_pixel(self.x, self.y, (self.hue, 1, 1))
            value = 0.6
            val_step = float(value/(self.tail_len+1))
            for x, y in self.tail:
                value -= val_step
                self.wall.set_pixel(x, y, (self.hue, 1, value))

        def advance(self):
            self.tail = [(self.x, self.y)] + self.tail[:self.tail_len-1]
            self.x += self.dx
            if self.x < 0:
                self.x = 1
                self.dx = -self.dx
            elif self.x >= self.wall.width:
                self.x = self.wall.width - 2
                self.dx = -self.dx

            self.y += self.dy
            if self.y < 0:
                self.y = 1
                self.dy = -self.dy
            elif self.y >= self.wall.height:
                self.y = self.wall.height - 2
                self.dy = -self.dy

    def run(self):
        if self.wall.width < 2 or self.wall.height < 2:
            return

        balls = []
        for i in range(3):
            balls.append(self.Ball(self.wall))

        start_time = time.time()
        while time.time() - start_time < 5:
            self.wall.clear()
            for ball in balls:
                ball.draw()
                ball.advance()
            self.wall.draw()
            time.sleep(.1)

class Message(Effect):
    message = [
        '                                                                      ',
        '     **  * * *** * *  ** *  *    *  **     **  **  ** *   * *         ',
        '     * * * *  *  * * * * ** *    * *      *   * * * * *   * *         ',
        '     **   *   *  *** * * * **    *  *     *   * * * * *   * *         ',
        '     *    *   *  * * * * *  *    *   *    *   * * * * *               ',
        '     *    *   *  * * **  *  *    * **      ** **  **  *** * *         ',
        ]

    def run(self):
        if self.wall.height < 6 or self.wall.width < 2:
            return

        col = 0
        start_time = time.time()
        while time.time() - start_time < 10:
            self.wall.clear()
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    if y >= len(self.message):
                        break
                    dot = self.message[y][(x+col) % len(self.message[0])]
                    if dot != ' ':
                        self.wall.set_pixel(x, y, (.333, 1, 1))
            self.wall.draw()
            col += 1
            time.sleep(0.07)

Effects = [SolidColorTest, HueTest, SaturationTest, ValueTest, DictionaryTest,
           LetterTest, Checkerboards, Columns, Rainbow, Twinkle, KnightMoves,
           Matrix, Bouncer, Message]
