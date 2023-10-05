from enum import Enum
import inspect
import pygame as pg
import sys

class InputEvent:
    def __init__(self, event: pg.event.Event):
        self.event = event
        self.key: int = event.key if hasattr(event, "key") else -1
        self.type: int = event.type if hasattr(event, "type") else -1
        self.button: int = event.button if hasattr(event, "button") else -1
    
    def __repr__(self):
        return f"InputEvent({self.event}) {self.key} {self.button} {self.type}"

def handleInput(event) -> InputEvent:
    inpEvent = InputEvent(event)

    if inpEvent.key == pg.K_ESCAPE:
        pg.quit()
        sys.exit()
    return inpEvent

