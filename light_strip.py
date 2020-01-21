from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from gpiozero import LED
import time
import _thread
import board
import neopixel

class Lights(Resource):
    def get(self):
        global color, state
        return {'state': state, 'color': color}, 200

    def put(self):
        global lights, state
        parser = reqparse.RequestParser()
        parser.add_argument('state')
        parser.add_argument('color')
        args = parser.parse_args()

        if (args['state']):
            new_state = args['state']
            if new_state == "on":
                lights.on()
                state = True
            elif new_state == "off":
                lights.off()
                update_color()
                state = False
            elif new_state == "toggle":
                self.toggle()
        if (args['color']):
            global color
            color = args['color']
            update_color()

        return 'Lights updated', 200

    def toggle(self):
        global lights, state
        if state:
            lights.off()
            update_color()
            state = False
        else:
            lights.on()
            state = True

def update_color():
    global color, strip
    r = int(color[0 : 2], 16)
    g = int(color[2 : 4], 16)
    b = int(color[4 : 6], 16)
    strip.fill((r, g, b))

lights = LED(4)
state = False

app = Flask(__name__)
api = Api(app)
CORS(app, origins='*')
api.add_resource(Lights, '/lights')

strip = neopixel.NeoPixel(board.D18, 487)
color = '000000'

if __name__ == '__main__':
    update_color()
    app.run(host='192.168.1.17', port=8082)