class DisabledSignal:
    """Inspired from https://bit.ly/3XaoBpx"""

    def __init__(self, signal, receiver, sender):
        self.signal = signal
        self.receiver = receiver
        self.sender = sender

    def __enter__(self):
        self.signal.disconnect(self.receiver, sender=self.sender)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.signal.connect(self.receiver, sender=self.sender)
