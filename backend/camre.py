import cv2
from picamera import Picamera2
def test_pi_camera():
    """
    Tests Raspberry Pi Camera Module 3 using Picamera2.
    """
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()

    print("Camera started. Press 'q' to quit.")
    while True:
        frame = picam2.capture_array()
        cv2.imshow("Pi Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    test_pi_camera()
