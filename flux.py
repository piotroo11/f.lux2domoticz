from bottle import run, post, request
import math
import requests

# CONFIG START

user = ''
password = ''
address = "http://192.168.0.122:8080"
deviceId = '32'

#CONFIG END

@post('/room_1')
def room_handler():
    post_dict = request.query.decode()
    if 'ct' in post_dict and 'bri' in post_dict:
        colour_temperature = int(post_dict['ct'])
        brightness = int(float(post_dict['bri']) * 100)

        # range check
        if colour_temperature < 1000:
            colour_temperature = 1000
        elif colour_temperature > 40000:
            colour_temperature = 40000

        tmp_internal = colour_temperature / 100.0

        # red
        if tmp_internal <= 66:
            red = 255
        else:
            tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
            if tmp_red < 0:
                red = 0
            elif tmp_red > 255:
                red = 255
            else:
                red = tmp_red

        # green
        if tmp_internal <= 66:
            tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
            if tmp_green < 0:
                green = 0
            elif tmp_green > 255:
                green = 255
            else:
                green = tmp_green
        else:
            tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
            if tmp_green < 0:
                green = 0
            elif tmp_green > 255:
                green = 255
            else:
                green = tmp_green

        # blue
        if tmp_internal >= 66:
            blue = 255
        elif tmp_internal <= 19:
            blue = 0
        else:
            tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
            if tmp_blue < 0:
                blue = 0
            elif tmp_blue > 255:
                blue = 255
            else:
                blue = tmp_blue

        RRGGBB = f'{int(round(red)):02x}{int(round(green)):02x}{int(round(blue)):02x}'
        seq = (address, "/json.htm?type=command&param=setcolbrightnessvalue&idx=", deviceId, "&hex=", str(RRGGBB), "&brightness=", str(brightness), "&iswhite=false")
        blankString = ''
        url = blankString.join(seq)
        response = requests.get(url, auth=(user, password))


run(host='localhost', port=8080)

