from psim.particle import EParticleType
from psim.math import Vector2D, Vector2DRot
from psim.entity import Entity
import psim as ps
import numpy as np
import pygame as pg
import math


class Simulation(Entity):
    def __init__(self):
        super().__init__(0, 0)
        self.particles = [ps.Particle(x=np.random.randint(0, ps.app.WIDTH/2), \
                                    y=np.random.randint(0, ps.app.HEIGHT/2), type=EParticleType.BLUE)\
                                    for _ in range(40)]

    def clicked(self, x, y, rand):
        typ = EParticleType.BLUE
        startVel = np.random.rand()
        print(startVel)
        if not rand:
            typ = EParticleType.RED
            startVel = 0
        self.particles.append(ps.Particle(Vector2D(x, y), \
                                            Vector2DRot(startVel, np.random.random() * 2 * math.pi),\
                                            typ))
    
    # !Overriding Entity! #
    def display(self):
        for p in self.particles:
            p.display()

    def update(self):
        pcache = []
        dcache = []

        avgVel = 0
        maxVel = 0
        minVel = 0
        avgPosX = 0
        avgPosY = 0
        avgCount = 0
        for i, e in enumerate(self.particles):
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
            for p in self.particles[i+1:]:
                newps = e.gravity(p)
                if newps:
                    if newps[0]:
                        pcache.append(newps[0])
                    if newps[1]:
                        pcache.append(newps[1])
                e.collide(p)

            # Move and query for photon
            e.move()
            avgVel += e.velocity
            # e.display()
        if avgCount == 0:
            avgCount = 1
        avgPosX = float(avgPosX / avgCount)
        avgPosY = float(avgPosY / avgCount)
        pg.draw.circle(ps.getScreen(), (0, 255, 0), (avgPosX, avgPosY), 10, 10)           
        deleted = 0
        for d in dcache:
            if d in self.particles:
                self.particles.remove(d)
                deleted += 1
        return (minVel, maxVel, avgVel, avgCount, avgPosX, avgPosY)
