from ultralytics import YOLO
import numpy as np
import cv2
import torch
import gc

torch.set_num_threads(1)  # evita que torch use múltiples hilos y dispare el uso de RAM

model = YOLO("models/epp_model.pt")

print("Clases del modelo:", model.names)

HARDHAT_CLASSES = {"Hardhat"}
MASK_CLASSES = {"Mask"}

def detect_epp(image_bytes: bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    with torch.no_grad():  # evita que se guarden gradientes en memoria (no los necesitas en inferencia)
        results = model(img, conf=0.4, imgsz=416)[0]  # imgsz más chico = menos memoria/más rápido

    helmet_detected = False
    mask_detected = False

    for box in results.boxes:
        class_name = model.names[int(box.cls[0])]
        confidence = float(box.conf[0])
        print(f"Detectado: '{class_name}' con confianza {confidence:.2f}")

        if class_name in HARDHAT_CLASSES:
            helmet_detected = True
        elif class_name in MASK_CLASSES:
            mask_detected = True

    del results, img, np_arr  # libera referencias explícitamente
    gc.collect()  # fuerza limpieza de memoria

    status = "COMPLIANT" if helmet_detected and mask_detected else "NON_COMPLIANT"

    return {
        "helmet_detected": helmet_detected,
        "mask_detected": mask_detected,
        "status": status
    }