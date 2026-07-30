"""
=========================================
Smart Traffic Monitoring System

Main Application

Author : Sharif Ullah
=========================================
"""


import cv2
import uuid



from detection.tracker import TrafficTracker
from detection.counter import VehicleCounter
from detection.speed import SpeedEstimator
from detection.density import TrafficDensity
from detection.violation import ViolationManager
from detection.line_counter import LineCounter



from database.database import TrafficDatabase





# ==========================
# Configuration
# ==========================


MODEL_PATH = "models/yolo11n.pt"

VIDEO_PATH = "videos/traffic.mp4"


SPEED_LIMIT = 10







def main():


    print("="*50)
    print("Smart Traffic Monitoring Started")
    print("="*50)



    # ==========================
    # Load Modules
    # ==========================


    tracker = TrafficTracker(
        MODEL_PATH
    )


    counter = VehicleCounter()


    speed_estimator = SpeedEstimator()


    density_estimator = TrafficDensity()


    violation_manager = ViolationManager()


    database = TrafficDatabase()



    print(
        "All Modules Loaded Successfully"
    )




    # ==========================
    # Create New Session
    # ==========================


    session_id = int(
        uuid.uuid4().int % 100000
    )


    print(
        "Session ID:",
        session_id
    )





    # ==========================
    # Open Video
    # ==========================


    cap = cv2.VideoCapture(
        VIDEO_PATH
    )


    if not cap.isOpened():

        print(
            "Video file not found"
        )

        return




    # Read first frame

    ret, first_frame = cap.read()


    if not ret:

        print(
            "Cannot read video"
        )

        return




    height, width = first_frame.shape[:2]



    # Dynamic center line

    line_y = height // 2




    line_counter = LineCounter(
        line_y=line_y
    )




    # Restart video

    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        0
    )




    print("\nVideo Started...")
    print("Press Q to Exit\n")




    # Store vehicles

    vehicle_records = {}



    # ==========================
    # Main Loop Start
    # ==========================


    while True:


        ret, frame = cap.read()



        if not ret:

            print(
                "Video Finished"
            )

            break



        
        # ==========================
        # YOLO Detection + Tracking
        # ==========================


        objects = tracker.track(
            frame
        )


        density = density_estimator.calculate(
            len(objects)
        )



        # ==========================
        # Draw Counting Line
        # ==========================


        cv2.line(

            frame,

            (0, line_y),

            (width, line_y),

            (255,0,0),

            3

        )




        # ==========================
        # Process Objects
        # ==========================


        for obj in objects:


            track_id = obj["id"]


            vehicle = obj["class"]


            x1,y1,x2,y2 = obj["bbox"]




            # Center Point

            center_x = int(
                (x1+x2)/2
            )

            center_y = int(
                (y1+y2)/2
            )




            # ======================
            # Vehicle Counter
            # ======================


            counter.update(

                track_id,

                vehicle

            )





            # ======================
            # Entry Exit
            # ======================


            direction = line_counter.update(

                track_id,

                center_x,

                center_y

            )



            entry = 0

            exit = 0



            if direction == "IN":

                entry = 1



            elif direction == "OUT":

                exit = 1





            # ======================
            # Speed
            # ======================


            speed = speed_estimator.calculate_speed(

                track_id,

                center_x,

                center_y

            )





            # ======================
            # Violation
            # ======================


            violation = "NO"


            if speed_estimator.is_overspeed(

                speed,

                SPEED_LIMIT

            ):

                violation = "YES"

                violation_manager.add_overspeed(

                    track_id,

                    speed

                )





            # ======================
            # Store Vehicle Data
            # ======================


            if track_id is not None:



                if track_id not in vehicle_records:


                    vehicle_records[track_id] = {

                        "vehicle": vehicle,
                        "speed": speed,
                        "violation": violation,
                        "density": density,
                        "entry":0,
                        "exit":0

                    }
                    database.insert_data(

                        session_id=session_id,

                        vehicle_id=track_id,

                        vehicle=vehicle,

                        speed=speed,

                        violation=violation,

                        density=density,

                        entry=0,

                        exit=0

                    )



                if entry == 1:

                    vehicle_records[track_id]["entry"] = 1



                if exit == 1:

                    vehicle_records[track_id]["exit"] = 1




                vehicle_records[track_id]["speed"] = speed
                # LIVE DATABASE UPDATE

                database.update_vehicle(

                    session_id,

                    track_id,

                    speed,

                    violation,

                    density,

                    entry,

                     exit

                )
                if violation == "YES":

                    vehicle_records[track_id]["violation"] = "YES"
                





            # ======================
            # Draw Bounding Box
            # ======================


            if violation == "YES":

                color = (0,0,255)

            else:

                color = (0,255,0)




            cv2.rectangle(

                frame,

                (x1,y1),

                (x2,y2),

                color,

                2

            )





            label = (

                f"{vehicle} "

                f"ID:{track_id} "

                f"{speed} km/h"

            )



            cv2.putText(

                frame,

                label,

                (x1,y1-10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (255,255,0),

                2

            )
        # ==========================
        # Live Dashboard Overlay
        # ==========================


        cv2.putText(

            frame,

            f"Vehicles : {counter.get_total()}",

            (20,40),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255,255,255),

            2

        )



        cv2.putText(

            frame,

            f"Density : {density}",

            (20,80),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0,255,255),

            2

        )



        cv2.putText(

            frame,

            f"Overspeed : {violation_manager.get_total_overspeed()}",

            (20,120),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0,0,255),

            2

        )



        cv2.putText(

            frame,

            f"Entry : {line_counter.entry_count}",

            (20,160),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0,255,0),

            2

        )



        cv2.putText(

            frame,

            f"Exit : {line_counter.exit_count}",

            (20,200),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255,0,0),

            2

        )




        # ==========================
        # Show Video
        # (FOR LOOP KE BAHAR)
        # ==========================


        cv2.imshow(

            "Smart Traffic Monitoring",

            frame

        )



        if cv2.waitKey(1) & 0xFF == ord("q"):

            break





    # ==========================
    # Save Database
    # ==========================
    print("\n================ Vehicle Records ================\n")

    for vid, data in vehicle_records.items():

        print(
            f"ID={vid} | "
            f"Speed={data['speed']} | "
            f"Violation={data['violation']}"
        )




    # ==========================
    # Close Everything
    # ==========================


    cap.release()


    cv2.destroyAllWindows()


    database.close()



    print(
        "\nProgram Closed Successfully"
    )






if __name__ == "__main__":

    main()