import psim
import random as rand
import pysimmy
from psim.simulation.fieldsimulation import FieldSimulation
from psim.simulation.particlesimulator import ParticleSimulation
from psim.simulation.sandsimulation import SandSimulation
from pysimmy import View
from pysimmy.Simulation import ParticleSimulator


def main():
    app = pysimmy.App(800, 600, 144)

    view = View(800, 600, 144)
    datalayer = pysimmy.getDataLayer()
    cacheId = datalayer.createCache([{'x': rand.random()*800, 'y': rand.random()*600} for _ in range(10)])
    app.addSimulation(ParticleSimulator(view, cacheId))

    app.start()

if __name__ == "__main__":
    main()

# from unitons import Uniton, PRIMES, AMOUNT

# def getUnitons():
#     AMOUNT
#     nums = []
#     for i in range(AMOUNT):
#         nums.append(Uniton(i))
#     return nums
# UNITONS = getUnitons()

# Notes:
# Prune chains during sleep
# Chemical signaling to other networks
# Periodic waves to add a temporal behavior
# Uncertainty / noise to all data

# Environment has criteria for survival