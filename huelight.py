from phue import Bridge


def hueConnect(value):
    bridge = Bridge("172.31.229.35")
    bridge.connect()
    lights = bridge.get_light_objects('name')
    lights["Hue Go"].on = True
    lights["Hue Go"].brightness = 254
    lights["Hue Go"].saturation = 255
    lights["Hue Go"].hue = value
