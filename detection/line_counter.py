"""
=========================================
Smart Traffic Monitoring System

Line Crossing Counter Module

Author : Sharif Ullah
=========================================
"""



class LineCounter:



    def __init__(self, line_y=300):


        self.line_y = line_y


        # Previous vehicle positions

        self.previous_positions = {}



        # Already counted IDs

        self.counted_entry = set()

        self.counted_exit = set()



        # Counters

        self.entry_count = 0

        self.exit_count = 0






    def update(

            self,

            track_id,

            center_x,

            center_y

    ):



        if track_id is None:

            return None





        direction = None





        if track_id in self.previous_positions:



            old_x, old_y = self.previous_positions[track_id]





            # Vehicle crosses downward

            if (

                old_y < self.line_y

                and

                center_y >= self.line_y

            ):



                if track_id not in self.counted_entry:



                    self.entry_count += 1


                    self.counted_entry.add(
                        track_id
                    )


                    direction = "IN"






            # Vehicle crosses upward

            elif (

                old_y > self.line_y

                and

                center_y <= self.line_y

            ):



                if track_id not in self.counted_exit:



                    self.exit_count += 1


                    self.counted_exit.add(
                        track_id
                    )


                    direction = "OUT"







        # Save current position

        self.previous_positions[track_id] = (

            center_x,

            center_y

        )



        return direction






    def reset(self):


        self.previous_positions.clear()


        self.counted_entry.clear()


        self.counted_exit.clear()


        self.entry_count = 0


        self.exit_count = 0