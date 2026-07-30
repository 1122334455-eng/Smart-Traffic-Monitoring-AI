"""
=========================================
Smart Traffic Monitoring System

Traffic Density Estimator

Author : Sharif Ullah
=========================================
"""


class TrafficDensity:


    def __init__(self):

        self.low_limit = 5
        self.medium_limit = 12

        self.max_capacity = 30



    def calculate(self, total_vehicles):

        """
        Calculate traffic density level
        """


        if total_vehicles <= self.low_limit:

            return "LOW"


        elif total_vehicles <= self.medium_limit:

            return "MEDIUM"


        else:

            return "HIGH"



    def calculate_percentage(
            self,
            total_vehicles
    ):

        """
        Calculate density percentage
        """

        percentage = (
            total_vehicles /
            self.max_capacity
        ) * 100


        if percentage > 100:

            percentage = 100



        return round(
            percentage,
            2
        )



    def get_signal_status(
            self,
            density
    ):

        """
        Traffic signal suggestion
        """


        if density == "LOW":

            return "GREEN"


        elif density == "MEDIUM":

            return "YELLOW"


        else:

            return "RED"