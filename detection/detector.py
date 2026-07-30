"""
=========================================
Smart Traffic Monitoring System
Main Detection Pipeline

Author : Sharif Ullah
=========================================
"""

import os
import cv2
from detection.speed import SpeedEstimator
from detection.violation import ViolationManager
from detection.density import TrafficDensity
from detection.traffic_signal import TrafficSignal
from detection.emergency import EmergencyManager

from config.config import (
    MODEL_PATH,
    VIDEO_PATH,
    OUTPUT_PATH,
    EMERGENCY_TEST,
    LINE_Y,
    LINE_COLOR,
    LINE_THICKNESS_COUNTER,
    SPEED_LIMIT,
    USE_WEBCAM,
    WEBCAM_INDEX
)

from detection.tracker import TrafficTracker
from detection.counter import VehicleCounter
from detection.line_counter import LineCounter
from database.database import TrafficDatabase
from database.session import SessionDatabase

from detection.utils import (
    FPSCounter,
    draw_box,
    draw_counter,
    draw_line
)
from reports.csv_report import CSVReport
from reports.excel_report import ExcelReport
from reports.pdf_report import PDFReport


def main():

    print("=" * 60)
    print("SMART TRAFFIC MONITORING SYSTEM")
    print("=" * 60)

    # -----------------------------------
    # Initialize Modules
    # -----------------------------------

    tracker = TrafficTracker(MODEL_PATH)

    counter = VehicleCounter()

    line_counter = LineCounter(LINE_Y)

    fps_counter = FPSCounter()
    speed_estimator = SpeedEstimator(
        pixel_to_meter=0.05
)
    density = TrafficDensity()
    traffic_signal = TrafficSignal()
    emergency_manager = EmergencyManager()

    violation_manager = ViolationManager()

    database = TrafficDatabase()
    session_db = SessionDatabase()

    session_id = session_db.create_session()


# Snapshot Folder
    snapshot_folder = "output/snapshots"

    os.makedirs(
        snapshot_folder,
        exist_ok=True
    )


    vehicle_classes = [
        "car",
        "truck",
        "bus",
        "motorcycle"
    ]

    # -----------------------------------
    # Open Video / Webcam
    # -----------------------------------



    if USE_WEBCAM:

        print("Starting Webcam Detection...")

        cap = cv2.VideoCapture(
            WEBCAM_INDEX
        )
        if not cap.isOpened():
            print("Camera not found")
            return

    else:

        print("Starting Video Detection...")

        cap = cv2.VideoCapture(
            str(VIDEO_PATH)
        )
        if not cap.isOpened():

            print("Unable to open Camera/Video")
            return

    # -----------------------------------
    # Video Properties
    # -----------------------------------

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    writer = cv2.VideoWriter(
        str(OUTPUT_PATH),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    print(
        f"Resolution : {width}x{height}"
    )

    print(
        f"FPS : {fps}"
    )


    total_frames = 0
    traffic_density = "LOW"
    saved_tracks = set()

    # -----------------------------------
    # Main Loop
    # -----------------------------------

    while True:

        success, frame = cap.read()

        if not success:
            break

        total_frames += 1

        draw_line(
            frame,
            LINE_Y,
            LINE_COLOR,
            LINE_THICKNESS_COUNTER
        )

        results = tracker.track(frame)

        fps = fps_counter.update()

        if len(results) == 0:

            writer.write(frame)

            continue

        result = results[0]

        # -----------------------------------
        # If no detections
        # -----------------------------------

        if result.boxes is None or len(result.boxes) == 0:

           writer.write(frame)

           continue

        boxes = result.boxes

        
        # ---------------------------------
        # Process Every Detection
        # -----------------------------------

        for box in boxes:

            # Ignore invalid tracking results
            if box.id is None:
                continue

            # Bounding Box Coordinates
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Tracking ID
            track_id = int(box.id.item())

            # Class ID
            class_id = int(box.cls.item())

            # Confidence
            confidence = float(box.conf.item())
            if confidence < 0.4:
                continue

            
            # Class Name
            class_name = tracker.model.names[class_id]
            # Check Emergency Vehicle

            if EMERGENCY_TEST:

                emergency_manager.emergency = True
                emergency_manager.vehicle = "AMBULANCE"

            else:

                emergency_manager.check(
                    class_name
                )


            

            # Ignore non vehicles
            if class_name not in vehicle_classes:
                continue
            


            # Count object only once
            counter.update(
                track_id,
                class_name
            )

            # Label
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)


            speed = speed_estimator.calculate_speed(
                track_id,
                center_x,
                center_y
            )
            overspeed = speed_estimator.is_overspeed(
                speed,
                SPEED_LIMIT
            )


            if overspeed:

                violation_manager.add_overspeed(track_id)

                violation = "YES"

                label = (
                    f"ID:{track_id} "
                    f"{class_name} "
                    f"OVERSPEED "
                    f"{speed} km/h"
                )

            else:

                violation = "NO"

                label = (
                    f"ID:{track_id} "
                    f"{class_name} "
                    f"{speed} km/h"
                )


# Save only once in database
            if track_id not in saved_tracks:

                database.insert_data(
                    session_id=session_id,
                    vehicle=class_name,
                    speed=speed,
                    violation=violation,
                    density=traffic_density,
                    entry=line_counter.get_entry_count(),
                    exit=line_counter.get_exit_count()
                )

                saved_tracks.add(track_id)

                vehicle_crop = frame[
                    int(y1):int(y2),
                    int(x1):int(x2)
                ]

                snapshot_path = os.path.join(
                    snapshot_folder,
                    f"{class_name}_{track_id}.jpg"
                )

                if vehicle_crop.size != 0:
                    vehicle_crop = cv2.resize(
                        vehicle_crop,
                        (300, 300)
                    )

                    cv2.imwrite(
                        snapshot_path,
                        vehicle_crop
                    )

            draw_box(
                frame,
                (x1, y1, x2, y2),
                label
            )

            cv2.circle(
               frame,
               (center_x, center_y),
               4,
               (0,255,255),
               -1
            )

            line_counter.update(
                track_id,
                center_x,
                center_y
            )
# -----------------------------------
# Traffic Density
# -----------------------------------

        current_vehicles = len(boxes)

        traffic_density = density.calculate(
            current_vehicles
        )
        signal = traffic_signal.update(
            traffic_density,
            emergency_manager.get_status()
        )
         

        # -----------------------------------
        # Draw Live Counter
        # -----------------------------------

        draw_counter(
            frame,
            counter.get_counts()
        )
        cv2.putText(
            frame,
            f"ENTRY : {line_counter.get_entry_count()}",
            (width-220,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"EXIT : {line_counter.get_exit_count()}",
            (width-220,90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )
        cv2.putText(
            frame,
            f"OVERSPEED : {violation_manager.get_total_overspeed()}",
            (width-220,130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )
        cv2.putText(
            frame,
            f"DENSITY : {traffic_density}",
            (width - 220, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
            )
        # -------------------------------
        # Traffic Signal
        # -------------------------------

        if signal == "GREEN":

            color = (0,255,0)

        elif signal == "YELLOW":

            color = (0,255,255)

        else:

            color = (0,0,255)


        cv2.putText(
            frame,
            f"SIGNAL : {signal}",
            (width-220,210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )


# -------------------------------
# Emergency Vehicle Status
# -------------------------------

        if emergency_manager.get_status():

            cv2.putText(
                frame,
                "EMERGENCY VEHICLE DETECTED",
                (width-350,250),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,0,255),
                2
            )


            cv2.putText(
                frame,
                "PRIORITY MODE ACTIVE",
                (width-300,290),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

        # -----------------------------------
        # Draw FPS
        # -----------------------------------

        cv2.putText(
            frame,
            f"FPS : {fps:.2f}",
            (10, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )


        # -----------------------------------
        # Save Output Frame
        # -----------------------------------

        writer.write(frame)

        # -----------------------------------
        # Show Live Video
        # -----------------------------------

        cv2.imshow(
            "Smart Traffic Monitoring",
            frame
        )

        # Press Q to Exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
           
    # -----------------------------------
    # Release Resources
    # -----------------------------------

    cap.release()

    writer.release()

    cv2.destroyAllWindows()
    


    # -----------------------------------
    # Final Report
    # -----------------------------------

    print("\n" + "=" * 50)

    print("Detection Completed")

    print("=" * 50)


    print(f"Total Frames Processed : {total_frames}")


    print("\nFINAL TRAFFIC COUNT")

    print("-" * 30)


    final_counts = counter.get_counts()


    for vehicle, count in final_counts.items():

        print(
            f"{vehicle} : {count}"
        )


    print("-" * 30)


    print(
        f"Total Objects : {counter.get_total()}"
    )
    print("\nLINE COUNTER")
    print("-"*30)

    print(f"Entry : {line_counter.get_entry_count()}")
    print(f"Exit  : {line_counter.get_exit_count()}")

    print("\nOVERSPEED VIOLATIONS")
    print("-" * 30)
    print(f"Total : {violation_manager.get_total_overspeed()}")

    print("\nTRAFFIC DENSITY")
    print("-" * 30)
    print(traffic_density)
    # ===============================
    # Generate Reports
    # ===============================

    traffic_data = database.fetch_all()


    print("\nGenerating Reports...\n")


    CSVReport().generate(
        traffic_data
    )


    ExcelReport().generate(
        traffic_data
    )


    PDFReport().generate(
        traffic_data
    )
    database.close()
    session_db.close()


    print("=" * 50)
    


print("\nOutput Video Saved Successfully!")

print(OUTPUT_PATH)



# =========================================
# Run Program
# =========================================

if __name__ == "__main__":

    main()