"""
=========================================
Emergency Vehicle Manager
=========================================
"""


class EmergencyManager:

    def __init__(self):

        self.emergency = False

        self.vehicle = "None"


    def check(self, class_name):

        emergency_list = [

            "ambulance",

            "fire truck",

            "police"

        ]


        if class_name.lower() in emergency_list:

            self.emergency = True

            self.vehicle = class_name

        else:

            self.emergency = False

            self.vehicle = "None"


        return self.emergency


    def get_status(self):

        return self.emergency


    def get_vehicle(self):

        return self.vehicle