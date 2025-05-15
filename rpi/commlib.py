import serial

class ArduinoComm:
    def __init__(self):
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 9600)
            print("init successful")
        except:
            raise ConnectionError("something went wrong with initializing communications")

    def sendData(self, data):
        self.arduino.write(data.encode())

    def recvData(self):
        received_data = self.arduino.readline().decode('utf-8').rstrip()
        return received_data

    def stop(self):
        self.arduino.close()
        return

class DummyComm:
    def __init__(self):
        self.arduino = None

    def sendData(self, data):
        # self.arduino.write(data.encode())
        print("tried to send: ",data)

    # def recvData(self):
        # received_data = self.arduino.readline().decode('utf-8').rstrip()
        # return received_data

    def stop(self):
        # self.arduino.close()
        return
