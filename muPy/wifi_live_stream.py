# check wifi module presence and live stream

import sensor, image, time, network, usocket

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.WVGA)
sensor.skip_frames(time = 2000)

SSID ='OPENMV_AP'
KEY  ='1234567890'
HOST = ''
PORT = 8080
streaming_duration = 10

wlan = None
try:
    wlan = network.WINC(mode=network.WINC.MODE_AP)
    wlan.start_ap(SSID, key=KEY, security=wlan.WEP, channel=2)
except OSError:
    pass
if wlan:
    def start_streaming(s):
        print ('Waiting for connections..')
    client, addr = s.accept()
    client.settimeout(2.0)
    print ('Connected to ' + addr[0] + ':' + str(addr[1]))
    data = client.recv(1024)
    client.send("HTTP/1.1 200 OK\r\n" \
                "Server: OpenMV\r\n" \
                "Content-Type: multipart/x-mixed-replace;boundary=openmv\r\n" \
                "Cache-Control: no-cache\r\n" \
                "Pragma: no-cache\r\n\r\n")
    clock = time.clock()
    start_time = time.time()
    print ('Successful connection time: ' + str(start_time))
    while (True):
        clock.tick()
        frame = sensor.snapshot()
        cframe = frame.compressed(quality=35)
        header = "\r\n--openmv\r\n" \
                 "Content-Type: image/jpeg\r\n"\
                 "Content-Length:"+str(cframe.size())+"\r\n\r\n"
        client.send(header)
        client.send(cframe)
        print(clock.fps())
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > streaming_duration:
            print("end of streaming")
            break
    while (True):
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    try:
        s.bind([HOST, PORT])
        s.listen(5)
        s.settimeout(3)
        start_streaming(s)
        print("live view terminated after pre-set" + str(streaming_duration) + " seconds")
    except OSError as e:
        s.close()
        print("socket error: ", e)
else:
     print("No WiFi")

clock = time.clock()


while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
