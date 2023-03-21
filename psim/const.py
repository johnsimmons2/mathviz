
class SystemValues:
    GRAV_CONST = 0.1
    SPEED_LIMIT = 1
    STRUCTURE_CONST = float(1/(120 + GRAV_CONST))
    WIDTH = 1920
    HEIGHT = 1080
    FPS = 120
    VIEW = None
    SCREEN = None
    COLORS = {
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'yellow': (198, 178, 50),
        'magenta': (160, 10, 160),
        'cyan': (50, 128, 200),
        'gray': (128, 128, 128)
    }

    SCHEME = {
        'background': COLORS['white'],
        'text': COLORS['black'],
        'debugline': COLORS['green'],
        'xaxis': COLORS['red'],
        'yaxis': COLORS['blue']
    }

    def getScreen(self):
        return self.SCREEN
    
    def getView(self):
        return self.VIEW
    
    def getDims(self):
        return (self.WIDTH, self.HEIGHT)


sysvals = SystemValues()
