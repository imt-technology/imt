import L76X
import time
import math

# Initialize GPS module
x = L76X.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)

x.L76X_Send_Command(x.SET_POS_FIX_400MS)
x.L76X_Send_Command(x.SET_NMEA_OUTPUT)
x.L76X_Exit_BackupMode()

# Initialize time
current_time = time.time()
m1 = math.floor(current_time / 60) % 60
h1 = math.floor(current_time / 3600) % 60
s1 = math.floor(current_time) % 60

if m1 >= 59:
    h1 += 1
    m1 = m1 + 1 - 60
else:
    m1 += 1

while True:
    x.L76X_Gat_GNRMC()
    
    if x.Status == 1:
        print('Already positioned')
    else:
        print('No positioning')
    
    print('Time {:02d}:{:02d}:{:02d}'.format(x.Time_H, x.Time_M, x.Time_S))
    print('Lon = {:.6f}, Lat = {:.6f}'.format(x.Lon, x.Lat))
    
    x.L76X_Baidu_Coordinates(x.Lat, x.Lon)
    print('Baidu coordinate {:.6f}, {:.6f}'.format(x.Lat_Baidu, x.Lon_Baidu))

    current_time = time.time()
    m = math.floor(current_time / 60) % 60
    h = math.floor(current_time / 3600) % 60
    s = math.floor(current_time) % 60

    if h >= h1 and m >= m1 and s >= s1:
        print("Enter backup mode \r\n")
        x.L76X_Send_Command(x.SET_PERPETUAL_BACKUP_MODE)
        
        print("Please enter any character to exit backup mode\r\n")
        input()
        print("Exit backup mode \r\n")
        x.L76X_Exit_BackupMode()

        # Reset timer for next backup
        current_time = time.time()
        m1 = math.floor(current_time / 60) % 60 + 1
        h1 = math.floor(current_time / 3600) % 60
        if m1 >= 59:
            h1 += 1
            m1 = m1 + 1 - 60
