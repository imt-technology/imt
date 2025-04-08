import cameralib
import commlib

if __name__ == "__main__":
    arduino = commlib.ArduinoComm()
    cameralib.get_cv2_stream()
