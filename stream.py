class Stream:
    def __init__(self, buffer):
        self.buffer = buffer
        self.caret = 0

    def read_u_short(self):
        value = (self.buffer[self.caret] << 8) + self.buffer[self.caret + 1]
        self.caret += 2
        return value

    def read_int(self):
        value = int.from_bytes(self.buffer[self.caret:self.caret+4], "big", signed=True)
        self.caret += 4
        return value
