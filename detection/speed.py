"""
=========================================
Smart Traffic Monitoring System
Speed Estimation Module

Author : Sharif Ullah
=========================================
"""

import time



class SpeedEstimator:


    def __init__(self, pixel_to_meter=0.5):

        self.pixel_to_meter = pixel_to_meter

        self.previous_positions = {}

        self.speeds = {}

        self.max_speeds = {}



    def calculate_speed(
        self,
        track_id,
        center_x,
        center_y
    ):


        if track_id is None:

            return 0



        current_time = time.time()


        speed = 0



        if track_id in self.previous_positions:


            old_x, old_y, old_time = (
                self.previous_positions[track_id]
            )


            distance_pixels = (
                (
                    (center_x - old_x) ** 2
                    +
                    (center_y - old_y) ** 2
                )
                ** 0.5
            )



            distance_meter = (
                distance_pixels *
                self.pixel_to_meter
            )



            time_difference = (
                current_time -
                old_time
            )



            if time_difference > 0:


                speed = (
                    distance_meter /
                    time_difference
                ) * 3.6



        # Save current position

        self.previous_positions[track_id] = (

            center_x,

            center_y,

            current_time
        )



        # Noise remove

        if speed < 0:

            speed = 0


        if speed > 150:

            speed = 0



        speed = round(speed,2)



        self.speeds[track_id] = speed



        # Maximum speed save

        if track_id not in self.max_speeds:

            self.max_speeds[track_id] = speed


        else:

            self.max_speeds[track_id] = max(
                self.max_speeds[track_id],
                speed
            )



        return speed




    def get_speed(self, track_id):

        return self.speeds.get(
            track_id,
            0
        )




    def get_max_speed(self, track_id):

        return self.max_speeds.get(
            track_id,
            0
        )




    def is_overspeed(
        self,
        speed,
        limit=80
    ):


        return speed > limit