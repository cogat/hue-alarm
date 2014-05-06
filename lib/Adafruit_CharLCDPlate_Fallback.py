class Adafruit_CharLCDPlate(object):

    # Port expander input pin definitions
    SELECT                  = 0
    RIGHT                   = 1
    DOWN                    = 2
    UP                      = 3
    LEFT                    = 4

    # LED colors
    OFF                     = 0x00
    RED                     = 0x01
    GREEN                   = 0x02
    BLUE                    = 0x04
    YELLOW                  = RED + GREEN
    TEAL                    = GREEN + BLUE
    VIOLET                  = RED + BLUE
    WHITE                   = RED + GREEN + BLUE
    ON                      = RED + GREEN + BLUE


    def __init__(self):
        self.colour = None

    def clear(self):
        self.message("")

    def message(self, msg):
        self.msg = msg
        self._display_msg()

    def _display_msg(self):
        msg = self.msg
        lines = msg.split("\n")[:2]
        if len(lines) < 2:
            lines.append("")

        print "-" * 4 + str(self.colour).ljust(14, "-")
        for line in lines:
            padded = line.ljust(16)[:16]
            print "|%s|" % padded
        print "-" * 18

    def backlight(self, colour):
        self.colour = colour
        self._display_msg()

    def buttonPressed(self, which):
        return False

