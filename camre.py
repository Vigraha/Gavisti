import cv2

def list_cameras():
    """
    Tests and prints all working camera indices.
    """
    working_cameras = []
    # Test a reasonable range of indices
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index: {i}")
            working_cameras.append(i)
            cap.release()
    if not working_cameras:
        print("No cameras found. Make sure your camera is connected and not in use by another application.")
    return working_cameras

if __name__ == '__main__':
    list_cameras()