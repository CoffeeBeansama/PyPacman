import pygame as pg

class EventHandler(object):
    
    pressingUp = False
    pressingDown = False
    pressingRight = False
    pressingLeft = False
    pressingMouseButton = False
    mousePos = None
    mousePressed = None
    keys = None

    @staticmethod
    def handlePlayerInput():
        EventHandler.keys = pg.key.get_pressed()

        EventHandler.mousePos = pg.mouse.get_pos()
        EventHandler.mousePressed = pg.mouse.get_pressed()

        EventHandler.pressingMouseButton = True if EventHandler.mousePressed[0] else False
        EventHandler.pressingUp = True if EventHandler.keys[pg.K_w] else False
        EventHandler.pressingDown = True if EventHandler.keys[pg.K_s] else False
        EventHandler.pressingLeft = True if EventHandler.keys[pg.K_a] else False
        EventHandler.pressingRight = True if EventHandler.keys[pg.K_d] else False
    
    def keyboardKeys():
        return EventHandler.keys

    def mousePosition():
        return EventHandler.mousePos
    
    def pressingLeftMouseButton():
        return EventHandler.pressingMouseButton

    def pressingUpKey():
        return EventHandler.pressingUp

    def pressingDownKey():
        return EventHandler.pressingDown

    def pressingLeftKey():
        return EventHandler.pressingLeft

    def pressingRightKey():
        return EventHandler.pressingRight
