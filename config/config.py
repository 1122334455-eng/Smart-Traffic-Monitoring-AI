"""
=========================================
Smart Traffic Monitoring System
Configuration File

Author : Sharif Ullah
=========================================
"""


from pathlib import Path



# =========================================
# Project Root Directory
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent



# =========================================
# Folder Paths
# =========================================

MODEL_DIR = PROJECT_ROOT / "models"

VIDEO_DIR = PROJECT_ROOT / "videos"

OUTPUT_DIR = PROJECT_ROOT / "output"



# Create output folder automatically

OUTPUT_DIR.mkdir(
    exist_ok=True
)



# =========================================
# File Paths
# =========================================

MODEL_PATH = MODEL_DIR / "yolo11n.pt"


VIDEO_PATH = VIDEO_DIR / "traffic.mp4"


OUTPUT_PATH = OUTPUT_DIR / "traffic_result.mp4"



# =========================================
# YOLO Settings
# =========================================

CONFIDENCE_THRESHOLD = 0.40


IOU_THRESHOLD = 0.50



# =========================================
# Tracker Settings
# =========================================

TRACKER_TYPE = "bytetrack.yaml"



# =========================================
# Display Settings
# =========================================

LINE_THICKNESS = 2


FONT_SCALE = 0.6


FONT_THICKNESS = 2



# =========================================
# Vehicle Classes
# =========================================

VEHICLE_CLASSES = [

    "car",

    "truck",

    "bus",

    "motorcycle",

    "bicycle"

]



# =========================================
# Colors (BGR)
# =========================================

BOX_COLOR = (
    0,
    255,
    0
)


TEXT_COLOR = (
    255,
    255,
    255
)
# ===========================================
# Line Counter Settings
# ===========================================

# Horizontal line position
LINE_Y = 200

# Line color (BGR)
LINE_COLOR = (0, 0, 255)

# Line thickness
LINE_THICKNESS_COUNTER = 3
# Speed Estimation

PIXEL_TO_METER = 0.05

FPS = 30

SPEED_LIMIT = 10
# ===========================================
# Speed Detection Settings
# ===========================================

SPEED_LIMIT = 10   # km/h

OVERSPEED_COLOR = (0, 0, 255)

NORMAL_SPEED_COLOR = (0, 255, 0)
# ==========================================
# Traffic Density Thresholds
# ==========================================

LOW_TRAFFIC = 5
MEDIUM_TRAFFIC = 12

# =====================================
# Input Source
# =====================================

# False = Video File
# True  = Live Webcam

USE_WEBCAM = False
WEBCAM_INDEX = 0
SNAPSHOT_FOLDER = "output/snapshots"
# Emergency Testing Mode

EMERGENCY_TEST = True