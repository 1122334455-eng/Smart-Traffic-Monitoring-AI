"""
=========================================
Smart Traffic Monitoring System
Violation Manager

Author : Sharif Ullah
=========================================
"""


import time



class ViolationManager:


    def __init__(self):


        # Store violations

        self.violations = []



        # Unique IDs

        self.overspeed_ids = set()

        self.signal_ids = set()

        self.direction_ids = set()



    # -------------------------------
    # Overspeed Violation
    # -------------------------------

    def add_overspeed(
            self,
            track_id,
            speed
    ):


        if track_id not in self.overspeed_ids:


            self.overspeed_ids.add(track_id)


            self.violations.append({

                "id": track_id,

                "type": "Overspeed",

                "value": speed,

                "time": time.strftime(
                    "%H:%M:%S"
                )

            })



    # -------------------------------
    # Signal Violation
    # -------------------------------

    def add_signal_violation(
            self,
            track_id
    ):


        if track_id not in self.signal_ids:


            self.signal_ids.add(track_id)


            self.violations.append({

                "id": track_id,

                "type": "Signal Break",

                "time": time.strftime(
                    "%H:%M:%S"
                )

            })



    # -------------------------------
    # Wrong Direction
    # -------------------------------

    def add_wrong_direction(
            self,
            track_id
    ):


        if track_id not in self.direction_ids:


            self.direction_ids.add(track_id)


            self.violations.append({

                "id": track_id,

                "type": "Wrong Direction",

                "time": time.strftime(
                    "%H:%M:%S"
                )

            })



    # -------------------------------
    # Get Violations
    # -------------------------------

    def get_all(self):

        return self.violations



    def get_total(self):

        return len(
            self.violations
        )



    def get_total_overspeed(self):

        return len(
            self.overspeed_ids
        )