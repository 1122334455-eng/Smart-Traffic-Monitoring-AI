"""
=========================================
Smart Traffic Monitoring System
Utility Functions

Author : Sharif Ullah
=========================================
"""


import cv2
import time

from config.config import (
    LINE_THICKNESS,
    FONT_SCALE,
    FONT_THICKNESS,
    BOX_COLOR,
    TEXT_COLOR
)



# =========================================
# FPS Calculator
# =========================================

class FPSCounter:

    def __init__(self):

        self.start_time = time.time()
        self.frames = 0
        self.fps = 0



    def update(self):

        self.frames += 1

        elapsed = time.time() - self.start_time


        if elapsed > 1:

            self.fps = self.frames / elapsed

            self.frames = 0

            self.start_time = time.time()


        return self.fps



# =========================================
# Draw Bounding Box
# =========================================

def draw_box(
        frame,
        box,
        label
):

    x1, y1, x2, y2 = map(
        int,
        box
    )


    cv2.rectangle(
        frame,
        (x1,y1),
        (x2,y2),
        BOX_COLOR,
        LINE_THICKNESS
    )


    cv2.putText(
        frame,
        label,
        (x1, y1-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        FONT_SCALE,
        TEXT_COLOR,
        FONT_THICKNESS
    )


    return frame



# =========================================
# Draw Counter Panel
# =========================================

def draw_counter(
        frame,
        counts
):

    y = 30


    cv2.rectangle(
        frame,
        (5,5),
        (220,170),
        (0,0,0),
        -1
    )


    cv2.putText(
        frame,
        "TRAFFIC COUNT",
        (15,y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        TEXT_COLOR,
        2
    )


    y += 30


    for key,value in counts.items():


        text = f"{key}: {value}"


        cv2.putText(
            frame,
            text,
            (15,y),
            cv2.FONT_HERSHEY_SIMPLEX,
            FONT_SCALE,
            TEXT_COLOR,
            FONT_THICKNESS
        )


        y += 25



    return frame



# =========================================
# Resize Frame
# =========================================

def resize_frame(
        frame,
        width=640
):

    height = int(
        frame.shape[0] *
        width /
        frame.shape[1]
    )


    return cv2.resize(
        frame,
        (width,height)
    )
def draw_line(frame, line_y, color, thickness):
    """
    Draw horizontal counting line
    """

    height, width = frame.shape[:2]

    cv2.line(
        frame,
        (0, line_y),
        (width, line_y),
        color,
        thickness
    )