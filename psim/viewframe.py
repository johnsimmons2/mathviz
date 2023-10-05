from enum import Enum
import pygame as pg
from psim.const import sysvals
from abc import abstractmethod
from psim.inputhandler import InputEvent


class ViewFrame:
    def __init__(self, width = None, height = None, fps = 144):
        pg.font.init()
        if width and height:
            self.width = width
            self.height = height
        else:
            self.width = sysvals.getDims()[0]
            self.height = sysvals.getDims()[1]
        self.FPSClock = pg.time.Clock()
        self.font = pg.font.Font('freesansbold.ttf', 16)
        self.entities: list = []
        self.display = pg.display.set_mode((self.width, self.height))
        self.simulation = False
        self.label = "entitylist"
        self.paused = False
        self.fps = fps
        self.debugmode = False
        self.active = False
        self._fpp = 1/(fps)
        self._cachedupdaterate = self._fpp
        self._pausedfps = 144
        self._cachefps = fps
        self._events: list[InputEvent] = []
        self._dt = 0
        self._t = pg.time.get_ticks()/1000

    def pushEvent(self, event: InputEvent):
        self._events.append(event)

    def setEntities(self, ents):
        self.entities = ents

    def setFPS(self, fps):
        self.fps = fps
        self._cachefps = fps
    
    def activate(self, val):
        print(self.label, val, "test")
        self.active = val
        self._t = pg.time.get_ticks()/1000.0
    
    def setUpdateRate(self, rate):
        self._fpp = rate
        self._cachedupdaterate = rate
    
    def addFPS(self, fps):
        if self.fps + fps > 144 or self.fps + fps < 0:
            return
        self.fps += fps
        self._cachefps += fps

    def pause(self):
        self.paused = not self.paused
        self._t = pg.time.get_ticks()/1000.0
        if self.paused:
            self.fps = self._pausedfps
            self._fpp = (1/self._pausedfps)
        else:
            self.fps = self._cachefps
            self._fpp = (self._cachedupdaterate)

    def update(self):
        stats = []
        if self.active:
            time = pg.time.get_ticks()/1000.0
            frametime = time - self._t
            self._dt += frametime
            self._t = time
            self._handleInputEvents()
            if not self.paused:
                if self._dt >= self._fpp:
                    stat = self._inner_update()
                    if stat != None:
                        stats.append(stat)
                    self._dt = 0.0

            for e in self.entities:
                e.display()
            self.FPSClock.tick(self.fps)
            self._inner_display()
            return stats if len(stats) > 0 else None
        else:
            self._t = pg.time.get_ticks()/1000.0
            return None

    @abstractmethod
    def _handleInputEvents(self):
        pass
    
    @abstractmethod
    def _inner_update(self):
        pass
        
    @abstractmethod
    def _inner_display(self):
        pass

class OptionType(Enum):
    DROPDOWN = 1
    CHECKBOX = 2

class OptionsView(ViewFrame):
    def __init__(self, width=None, height=None, fps=30):
        super().__init__(width, height, fps)
        self.options = {
            "Global Option 1": {
                "type": OptionType.DROPDOWN,
                "values": ["Option A", "Option B", "Option C"],
                "selected": 0
            },
            "Global Option 2": {
                "type": OptionType.CHECKBOX,
                "value": False
            },
            # Add more options as needed
        }
        self.selected_option = 0  # Index of the currently selected option

    def _handleInputEvents(self):
        for event in self._events:
            if event.key == pg.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pg.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pg.K_RETURN:
                self._handleOptionSelect()

    def _handleOptionSelect(self):
        selected_option_data = self.options[list(self.options.keys())[self.selected_option]]
        option_type = selected_option_data["type"]

        if option_type == OptionType.DROPDOWN:
            # Handle dropdown selection logic
            selected_value = selected_option_data["values"][selected_option_data["selected"]]
            print(f"Selected option: {selected_value}")
        elif option_type == OptionType.CHECKBOX:
            # Handle checkbox toggle logic
            selected_option_data["value"] = not selected_option_data["value"]
            print(f"Checkbox state: {selected_option_data['value']}")

    def _inner_update(self):
        pass

    def _inner_display(self):
        self.display.fill((255, 255, 255))  # Clear the screen

        # Display options
        y_offset = 50
        for idx, (option_name, option_data) in enumerate(self.options.items()):
            label = self.font.render(option_name, True, (0, 0, 0))
            self.display.blit(label, (20, y_offset))

            if idx == self.selected_option:
                # Highlight the selected option
                pg.draw.rect(self.display, (200, 200, 200), (150, y_offset, 200, 30))

            y_offset += 40

        pg.display.flip()

    def click_at(self, dx, dy, ext):
        pass  # Options view doesn't handle clicks for now