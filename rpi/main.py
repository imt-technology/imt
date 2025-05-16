import cameralib
import commlib
from newrobotcomm import *
import platform

system_name = platform.system()
release_info = platform.release()
RUNNING_ON_RPI = (system_name == 'Linux' and ('raspbian' in release_info.lower() or 'rpi' in release_info.lower()))

if __name__ == "__main__":
    if RUNNING_ON_RPI:
        import sensorlib
        arduino = commlib.ArduinoComm()
    else:
        arudino = commlib.DummyComm()
    cam1 = cameralib.get_cv2_stream()

    temperatura, vlaznost, radioaktivnost, radar_vrednost, radar_ugao = 0, 0, 0, 0, 0
    # asyncio.run(send_sensor_data(""))
    async def main():
        token = await login()
        if token:
            await asyncio.gather(send_gps_data(token), send_sensor_data(token, arduino), stream_video(cam1, token), listen_for_commands(token, arduino))
        else:
            print("❌ Neuspešan login, prekidam program.")

    asyncio.run(main())
