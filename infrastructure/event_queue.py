class EventQueue:
    def __init__(self):
        self._queue = []

    def push(self, event):
        self._queue.append(event)

    def pop_all(self):
        events = self._queue[:]
        self._queue.clear()
        return events