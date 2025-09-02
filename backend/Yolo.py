from ultralytics import YOLO
import cv2
import threading

# Define paths
weights_path = r"/home/pfdt5/Downloads/best"

# Load the YOLOv8 model
model = YOLO(weights_path)

# Initialize camera
cap = cv2.VideoCapture(0)

# Global variables to manage frame processing
output_frame = None
lock = threading.Lock()

def process_video_stream():
    """
    Function to return the latest processed frame.
    """
    global output_frame, lock
    with lock:
        frame_copy = output_frame.copy() if output_frame is not None else None
    return frame_copy

def run_detection_loop():
    """
    The main loop for object detection.
    """
    global output_frame, lock

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            results = model.predict(frame, conf=0.6, iou=0.5, imgsz=320, half=False, verbose=False)
            annotated_frame = results[0].plot(labels=True, conf=True)

            with lock:
                output_frame = annotated_frame.copy()

    finally:
        cap.release()
        print("Camera processing loop stopped.")

# Start the detection loop in a separate thread
thread = threading.Thread(target=run_detection_loop)
thread.daemon = True
thread.start()

# Note: The main script can now be started, and it will run the detection loop
# in the background. The Flask app will import and use the `process_video_stream` function.
