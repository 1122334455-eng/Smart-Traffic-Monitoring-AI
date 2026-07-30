"""
=========================================
Smart Traffic Monitoring System
Vehicle Counter Module

Author : Sharif Ullah
=========================================
"""


from collections import defaultdict



class VehicleCounter:


    def __init__(self):

        # Already counted vehicle IDs
        self.counted_ids = set()


        # Vehicle class counts
        self.class_counts = defaultdict(int)


        # Allowed traffic objects

        self.vehicle_classes = [

            "car",
            "truck",
            "bus",
            "motorcycle",
            "bicycle"

        ]



    def update(self, track_id, class_name):

        """
        Count vehicles only once
        """


        if track_id is None:
            return



        # Ignore non vehicles

        if class_name not in self.vehicle_classes:
            return



        # New vehicle detected

        if track_id not in self.counted_ids:


            self.counted_ids.add(track_id)


            self.class_counts[class_name] += 1



    def get_counts(self):

        return dict(
            self.class_counts
        )



    def get_total(self):

        return sum(
            self.class_counts.values()
        )



    def reset(self):

        self.counted_ids.clear()

        self.class_counts.clear()