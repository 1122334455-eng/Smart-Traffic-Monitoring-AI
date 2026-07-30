"""
=========================================
Traffic Signal Simulation
=========================================
"""

class TrafficSignal:

    def __init__(self):

        self.signal = "GREEN"


    def update(self, density, emergency=False):

        # Emergency Priority Mode

        if emergency:

            self.signal = "GREEN"

            return self.signal


        # Normal Traffic Logic

        if density == "LOW":

            self.signal = "GREEN"


        elif density == "MEDIUM":

            self.signal = "YELLOW"


        else:

            self.signal = "RED"


        return self.signal



    def get_signal(self):

        return self.signal