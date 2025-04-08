import cameralib
import commlib
import sensorlib

if __name__ == "__main__":
    arduino = commlib.ArduinoComm()
    cameralib.get_cv2_stream()
