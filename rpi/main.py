import cameralib
import commlib
import sensorlib
from servercomm import *

if __name__ == "__main__":
    arduino = commlib.ArduinoComm()
    cam1 = cameralib.get_cv2_stream()

    async def main():
        token = await login()
        if token:
            await asyncio.gather(send_gps_data(token), send_sensor_data(token, 0, 0, 0, 0, 0), stream_video(cam1, cam1, token), listen_for_commands(token))
        else:
            print("❌ Neuspešan login, prekidam program.")

    asyncio.run(main())
