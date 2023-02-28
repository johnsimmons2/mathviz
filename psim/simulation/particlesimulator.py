from psim.inputhandler import InputEvent
from psim.particle import EParticleType, Particle
from psim.simulation.simulation import Simulation


class ParticleSimulation(Simulation):
    def __init__(self, numParticles):
        super().__init__()
        self.entities = [Particle(type=EParticleType.BLUE) for _ in range(numParticles)]
        self.label = "Particle Simulation"
    
    def _handleInputEvents(self):
        for e in self._events:
            match(e):
                case InputEvent.KEY_SPACE:
                    self.pause()
                    continue
        self._events = []

    # !Override ViewFrame! #
    def _inner_update(self):
        pcache = []
        dcache = []

        avgVel = 0
        maxVel = 0
        minVel = 0
        avgPosX = 0
        avgPosY = 0
        avgCount = 0
        for i, e in enumerate(self.entities):
            if not isinstance(e, Particle):
                continue
            if not e.active:
                dcache.append(e)
                continue
            if e.velocity > maxVel:
                maxVel = e.velocity
            elif e.velocity < minVel:
                minVel = e.velocity
            avgPosX += e.x
            avgPosY += e.y
            avgCount += 1

            # Apply G force
            for p in self.entities[i+1:]:
                newps = e.gravity(p)
                if newps:
                    if newps[0]:
                        pcache.append(newps[0])
                    if newps[1]:
                        pcache.append(newps[1])
                e.collide(p)

            e.move()
            avgVel += e.velocity
        if avgCount == 0:
            avgCount = 1
        avgPosX = float(avgPosX / avgCount)
        avgPosY = float(avgPosY / avgCount)
        self._draw_circle((0, 255, 0), (avgPosX, avgPosY), 10)           
        deleted = 0
        for d in dcache:
            if d in self.entities:
                self.entities.remove(d)
                deleted += 1
        return (minVel, maxVel, avgVel, avgCount, avgPosX, avgPosY)