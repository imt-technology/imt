import logging
import asyncio
import cv2
import base64
import requests
import random
import time
from signalrcore.hub_connection_builder import HubConnectionBuilder

# 📌 API URL-ovi
AUTH_URL = "http://192.168.100.8:5000/api/users/login"
VIDEO_SIGNALR_URL = "ws://192.168.100.8:5000/videoHub"
GPS_SIGNALR_URL = "ws://192.168.100.8:5000/gpsHub"
SENSOR_SIGNALR_URL = "ws://192.168.100.8:5000/sensorHub"
CONTROL_SIGNALR_URL = "ws://192.168.100.8:5000/controlHub"

# 📌 Kamera na telefonu (IP Webcam app)
VIDEO_STREAM_PHONE = "http://192.168.100.11:8080/video"

# 📌 Kamera na laptopu (integrisana kamera)
CAMERA_LAPTOP = 0

# 📌 Početne vrednosti
DEVICE_ID = "autic_01"
latitude = 44.7866
longitude = 20.4489
temperature = 25.0
humidity = 60.0
radioactivity = 0.12
radar_value = 5.0
water_detected = 0
mine_detected = 0

# 📌 Postavke kvaliteta slike
JPEG_QUALITY = 50
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

async def login():
    """ Autentifikacija i dobijanje JWT tokena """
    payload = {"email": "...", "password": "..."}
    with open("CREDENTIALS","r") as f:
        raw = f.read()

    payload["email"] = raw.split("\n")[0]
    payload["password"] = raw.split("\n")[0]
    try:
        response = requests.post(AUTH_URL, json=payload, verify=False)
        response.raise_for_status()
        token = response.json().get("token")
        print(f"✅ Uspešan login! JWT token: {token[:30]}...")
        return token
    except requests.exceptions.RequestException as e:
        print("❌ Greška pri autentifikaciji!", str(e))
        return None

def connect_signalr(url, token):
    """ Povezivanje na SignalR sa JWT tokenom """
    full_url = f"{url}?access_token={token}"
    try:
        hub_connection = HubConnectionBuilder()\
            .with_url(full_url, options={"verify_ssl": False})\
            .with_automatic_reconnect({"type": "raw"})\
            .configure_logging(logging.INFO)\
            .build()

        hub_connection.start()
        print(f"✅ Povezano na SignalR: {url}")

        hub_connection.on_open(lambda: print("🔗 SignalR konekcija uspostavljena"))
        hub_connection.on_close(lambda: print("🔴 SignalR konekcija zatvorena"))

        return hub_connection

    except Exception as e:
        print(f"❌ Greška pri povezivanju: {e}, pokušavam ponovo...")
        return None

async def send_gps_data(token):
    """ Slanje GPS podataka preko SignalR-a. """
    client = connect_signalr(GPS_SIGNALR_URL, token)

    if client is None:
        print("❌ GPS SignalR konekcija nije uspostavljena.")
        return

    global latitude, longitude

    try:
        while True:
            latitude += random.uniform(-0.0005, 0.0005)
            longitude += random.uniform(-0.0005, 0.0005)

            print(f"📡 Slanje GPS podataka: {DEVICE_ID} - {latitude}, {longitude}")

            client.send("SendGpsData", [DEVICE_ID, str(latitude), str(longitude)])

            await asyncio.sleep(2)

    except Exception as e:
        print(f"❌ Greška u send_gps_data: {e}")

    finally:
        client.stop()
        print("🔴 SignalR GPS konekcija zatvorena!")

async def send_sensor_data(token, temperatura, vlaznost, radioaktivnost, radar_vrednost, radar_ugao):
    """ Slanje podataka sa senzora: temperatura, vlaznost, radioaktivnost, radar, voda, metal detekcija. """
    client = connect_signalr(SENSOR_SIGNALR_URL, token)

    if client is None:
        print("❌ Sensor SignalR konekcija nije uspostavljena.")
        return

    try:
        while True:
            # 📡 Simulacija podataka sa senzora

            # 🛑 Simulacija detekcije metala i vode
            voda = "0"
            metal = "0"

            trenutak = int(time.time()) % 180  # Broj sekundi u 3 minuta

            if 20 <= trenutak < 30:  # Voda se detektuje od 1:00 do 1:10
                voda = "1"
            if 30 <= trenutak < 40:  # Metal se detektuje od 2:00 do 2:20
                metal = "1"

            print(f"📡 Slanje podataka: Temp {temperatura}°C, Vlaznost {vlaznost}%, Rad {radioaktivnost} Sv/h, Radar [{radar_vrednost}, {radar_ugao}°], Voda {voda}, Metal {metal}")

            # 📤 Slanje podataka ka `sensorHub`
            client.send("SendTemperatureHumidity", [temperatura, vlaznost])
            client.send("SendSensorData", ["radioaktivnost", str(radioaktivnost)])
            client.send("SendSensorData", ["voda", voda])
            client.send("SendSensorData", ["metal", metal])

            # 📡 Slanje radarskih podataka (vrednost + ugao)
            client.send("SendRadarData", [radar_ugao, radar_vrednost])

            await asyncio.sleep(5)  # Pauza između slanja podataka

    except Exception as e:
        print(f"❌ Greška u send_sensor_data: {e}")

    finally:
        client.stop()
        print("🔴 SignalR Sensor konekcija zatvorena!")


def process_frame(frame):
    """ Obrada slike: smanjenje rezolucije i kvaliteta """
    frame_resized = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    _, buffer = cv2.imencode(".jpg", frame_resized, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
    frame_data = base64.b64encode(buffer).decode("utf-8")
    return frame_data

async def stream_video(token, cap_pi, cap_laptop): # no questions
    """ Slanje video frejmova sa telefona i laptopa preko SignalR-a """
    client = connect_signalr(VIDEO_SIGNALR_URL, token)

    if client is None:
        print("❌ Video SignalR konekcija nije uspostavljena.")
        return

    try:
        while True:
            frame_phone = cap_pi.capture_array()
            if cap_pi:
                frame_data = process_frame(frame_phone)
                client.send("SendVideoFrame", ["phone", frame_data])

            # ret_laptop, frame_laptop = cap_laptop.read() if cap_laptop.isOpened() else (False, None)
            # if ret_laptop:
                # frame_data = process_frame(frame_laptop)
                # client.send("SendVideoFrame", ["laptop", frame_data])
                # print("📡 Poslat video frejm sa laptop kamere!")

            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"❌ Greška u stream_video: {e}")

    finally:
        cap_phone.release()
        cap_laptop.release()
        client.stop()
        print("🔴 SignalR video konekcija zatvorena!")

async def listen_for_commands(token):
    """ Osluškivanje komandi za upravljanje """
    client = connect_signalr(CONTROL_SIGNALR_URL, token)

    def handle_command(tip, komanda):
        print(f"🕹️ Primljena komanda: ({tip} - {komanda})")

    client.on("ReceiveControlCommand", print)
