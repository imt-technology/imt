import cv2
import platform
import time

def get_cv2_stream():
    system_name = platform.system()
    release_info = platform.release()
    is_raspberry_pi = (system_name == 'Linux' and ('raspbian' in release_info.lower() or 'rpi' in release_info.lower()))

    if is_raspberry_pi:
        try:
            from picamera2 import Picamera2
            import numpy as np

            picam2 = Picamera2()
            config = picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)})
            picam2.configure(config)
            picam2.start()
            return 0, picam2
        except ImportError:
            print("Warning: picamera library not found. Falling back to default camera.")
            cap = cv2.VideoCapture(0)
            return 1, cap
        except Exception as e:
            print(f"error using Raspberry Pi camera: {e}. Falling back to default camera.")
            cap = cv2.VideoCapture(0)
            # if not cap.isOpened():
            #     raise IOError("cannot open default camera")
            # while True:
            #     ret, frame = cap.read()
            #     if not ret:
            #         break
            #     yield frame
            # cap.release()
            return 1, cap
    else:
        print("not running on a Raspberry Pi. using default camera.")
        cap = cv2.VideoCapture(0)
        # if not cap.isOpened():
        #     raise IOError("cannot open default camera")
        # while True:
        #     ret, frame = cap.read()
        #     if not ret:
        #         break
        #     yield frame
        # cap.release()
        return 1, cap

if __name__ == "__main__":
    print("this script is meant to be ran as a library.")
    print("however, it can function as a debug tool for the built in camera.")
    if input("continue? [y/N] ") == "y":
        stream_generator = get_cv2_stream()
        if stream_generator[0] == 1:
            try:
                while True:
                    ret, frame = stream_generator[1].read()
                    if not ret:
                        break
                    cv2.imshow("Camera Stream", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            finally:
                cv2.destroyAllWindows()
        else:
            while True:
                frame = stream_generator[1].capture_array()
                cv2.imshow("Camera Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    else:
        print("alright")
