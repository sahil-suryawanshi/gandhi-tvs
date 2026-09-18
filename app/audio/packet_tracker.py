class PacketTracker:
    def __init__(self):
        self.last_sequence = None
        self.dropped_packets = 0

    def add_packet(self, sequence_number: int) -> bool:
        if self.last_sequence is None:
            self.last_sequence = sequence_number
            return True

        expected_sequence = self.last_sequence + 1

        if sequence_number != expected_sequence:
            if sequence_number > expected_sequence:
                self.dropped_packets += sequence_number - expected_sequence

            self.last_sequence = sequence_number
            return False

        self.last_sequence = sequence_number
        return True

    def get_dropped_packets(self) -> int:
        return self.dropped_packets

    def reset(self):
        self.last_sequence = None
        self.dropped_packets = 0