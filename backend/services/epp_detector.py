from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO("models/epp_model.pt")

HARDHAT_CLASSES = {"Hardhat"}
MASK_CLASSES = {"Mask"}

def detect_epp(image_bytes: bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(img, conf=0.4)[0]

    helmet_detected = False
    mask_detected = False

    for box in results.boxes:
        class_name = model.names[int(box.cls[0])]
        if class_name in HARDHAT_CLASSES:
            helmet_detected = True
        elif class_name in MASK_CLASSES:
            mask_detected = True

    status = "COMPLIANT" if helmet_detected and mask_detected else "NON_COMPLIANT"

    return {
        "helmet_detected": helmet_detected,
        "mask_detected": mask_detected,
        "status": status
    }