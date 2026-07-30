"""
=========================================
Smart Traffic Monitoring System
ByteTrack Module

Author : Sharif Ullah
=========================================
"""

from ultralytics import YOLO

from config.config import (
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
    TRACKER_TYPE
)


class TrafficTracker:

    def __init__(self, model_path):

        print("=" * 50)
        print("Loading YOLO Model...")
        print("=" * 50)

        self.model = YOLO(str(model_path))

        print("YOLO Loaded Successfully\n")


    def track(self, frame):
        """
        Detect + Track objects
        """

        results = self.model.track(
            frame,
            persist=True,
            tracker=TRACKER_TYPE,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False
        )


        objects = []


        for result in results:

            boxes = result.boxes


            if boxes is None:
                continue


            for box in boxes:

                # Class ID
                cls_id = int(box.cls[0])


                # Object Name
                label = self.model.names[cls_id]


                # Confidence
                confidence = float(box.conf[0])


                # Tracking ID
                track_id = None

                if box.id is not None:
                    track_id = int(box.id[0])


                # Bounding Box

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                objects.append({

                    "id": track_id,

                    "class": label,

                    "confidence": round(
                        confidence, 2
                    ),

                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2
                    ]

                })


        return objects